package export

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"sync"
	"time"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
	"github.com/sirupsen/logrus"
	"github.com/xuri/excelize/v2"
)

// 定义常量
const (
	ExportDir = "exports"
	CacheDir  = "cache"
	BatchSize = 5000
)

// DBConfig 数据库配置
type DBConfig struct {
	Host     string
	Port     int
	User     string
	Password string
	Database string
}

// ChannelInfo 渠道信息
type ChannelInfo struct {
	ChannelCode string  `json:"channelCode"`
	Price       float64 `json:"price"`
}

// ItemDBModel 数据模型
type ItemDBModel struct {
	CargoNum        string    `gorm:"column:cargo_num"`
	CnName          string    `gorm:"column:cn_name"`
	MainUnitName    string    `gorm:"column:main_unit_name"`
	Spec            string    `gorm:"column:spec"`
	Delivery        string    `gorm:"column:delivery"`
	BrandName       string    `gorm:"column:brand_name"`
	Purity          string    `gorm:"column:purity"`
	OpType          string    `gorm:"column:op_type"`
	CasNo           string    `gorm:"column:cas_no"`
	LongDesc        string    `gorm:"column:long_desc"`
	ChannelInfoList string    `gorm:"column:channel_info_list"` // JSON string
	UpdatedAt       time.Time `gorm:"column:updated_at"`
}

// ExcelItemDBModel 缓存数据模型
type ExcelItemDBModel struct {
	ProductID        string  `gorm:"column:product_id"`
	CargoNum         string  `gorm:"column:cargo_num"`
	UnitPrice        float64 `gorm:"column:unit_price"`
	Category         string  `gorm:"column:category"`
	StorageCondition string  `gorm:"column:storage_condition"`
}

// ItemExportTask 导出任务结构体
type ItemExportTask struct {
	db          *gorm.DB
	channelCode string
	cachedItems map[string]ExcelItemDBModel
	deliveryMap map[string]string
	brandMap    map[string]string
	logger      *logrus.Logger
}

// NewItemExportTask 创建新的导出任务实例
func NewItemExportTask(dbConfig DBConfig, channelCode string) (*ItemExportTask, error) {
	// 创建必要的目录
	for _, dir := range []string{ExportDir, CacheDir} {
		if err := os.MkdirAll(dir, 0755); err != nil {
			return nil, fmt.Errorf("failed to create directory %s: %v", dir, err)
		}
	}

	// 连接数据库
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		dbConfig.User, dbConfig.Password, dbConfig.Host, dbConfig.Port, dbConfig.Database)

	db, err := gorm.Open("mysql", dsn)
	if err != nil {
		return nil, fmt.Errorf("failed to connect database: %v", err)
	}

	// 初始化logger
	logger := logrus.New()
	logger.SetFormatter(&logrus.TextFormatter{
		FullTimestamp: true,
	})

	task := &ItemExportTask{
		db:          db,
		channelCode: channelCode,
		cachedItems: make(map[string]ExcelItemDBModel),
		deliveryMap: initDeliveryMap(),
		brandMap:    initBrandMap(),
		logger:      logger,
	}

	// 加载缓存
	if err := task.loadCache(); err != nil {
		return nil, err
	}

	return task, nil
}

// loadCache 加载缓存数据
func (t *ItemExportTask) loadCache() error {
	cacheFile := filepath.Join(CacheDir, "excel_items_cache.pkl")

	// 检查缓存文件是否存在
	if _, err := os.Stat(cacheFile); err == nil {
		// 读取缓存文件
		data, err := os.ReadFile(cacheFile)
		if err != nil {
			return fmt.Errorf("failed to read cache file: %v", err)
		}

		// 解析缓存数据
		var items []ExcelItemDBModel
		if err := json.Unmarshal(data, &items); err != nil {
			return fmt.Errorf("failed to unmarshal cache data: %v", err)
		}

		// 将数据加载到内存缓存
		for _, item := range items {
			t.cachedItems[item.CargoNum] = item
		}

		t.logger.Infof("Loaded %d items from cache file", len(items))
		return nil
	}

	// 如果缓存文件不存在，从数据库创建缓存
	t.logger.Info("Cache file not found, creating from database")
	var items []ExcelItemDBModel
	if err := t.db.Find(&items).Error; err != nil {
		return fmt.Errorf("failed to fetch items from database: %v", err)
	}

	// 保存到内存缓存
	for _, item := range items {
		t.cachedItems[item.CargoNum] = item
	}

	// 将数据序列化
	data, err := json.Marshal(items)
	if err != nil {
		return fmt.Errorf("failed to marshal cache data: %v", err)
	}

	// 保存到缓存文件
	if err := os.WriteFile(cacheFile, data, 0644); err != nil {
		return fmt.Errorf("failed to write cache file: %v", err)
	}

	t.logger.Infof("Created cache with %d items", len(items))
	return nil
}

// getChannelPrice 获取指定渠道的价格
func (t *ItemExportTask) getChannelPrice(channelInfoJSON string) (float64, error) {
	var channelInfoList []ChannelInfo
	if err := json.Unmarshal([]byte(channelInfoJSON), &channelInfoList); err != nil {
		return 0, err
	}

	for _, info := range channelInfoList {
		if info.ChannelCode == t.channelCode {
			return info.Price, nil
		}
	}
	return 0, nil
}

// transformData 转换数据格式
func (t *ItemExportTask) transformData(items []ItemDBModel) []map[string]interface{} {
	var transformedData []map[string]interface{}

	for _, item := range items {
		price, err := t.getChannelPrice(item.ChannelInfoList)
		if err != nil {
			t.logger.Warnf("Failed to get channel price for item %s: %v", item.CargoNum, err)
			continue
		}

		cachedItem, exists := t.cachedItems[item.CargoNum]
		productID := ""
		if exists {
			productID = cachedItem.ProductID
		}

		delivery := t.deliveryMap[item.Delivery]
		if delivery == "" {
			// t.logger.Infof("Skipping item %s due to invalid delivery cycle: %s", item.CargoNum, item.Delivery)
			continue
		}

		transformedItem := map[string]interface{}{
			"product_id":        productID,
			"cargo_num":         truncateString(item.CargoNum, 30),
			"product_name":      truncateString(item.CnName, 40),
			"package_unit":      truncateString(item.MainUnitName, 2),
			"spec":              truncateString(item.Spec, 40),
			"delivery_cycle":    delivery,
			"list_price":        price,
			"unit_price":        price,
			"brand":             t.brandMap[item.BrandName],
			"category":          "实验试剂 - 其他",
			"description":       truncateString(item.CnName, 40),
			"storage_condition": "",
			"purity":            truncateString(item.Purity, 4),
			"status":            item.OpType,
			"cas_no":            truncateString(item.CasNo, 20),
			"tips":              truncateString(item.LongDesc, 1500),
		}

		transformedData = append(transformedData, transformedItem)
	}

	return transformedData
}

// exportBatch 导出单个批次数据
func (t *ItemExportTask) exportBatch(data []map[string]interface{}, batchNum int) (string, error) {
	f := excelize.NewFile()
	sheet := "商品数据"
	f.NewSheet(sheet)

	// 设置表头
	headers := []string{
		"商品ID", "货号", "商品名称", "包装单位", "规格",
		"供货周期", "目录价", "单价", "品牌", "二级分类",
		"商品描述", "存储条件", "纯度", "状态", "CAS号", "提示",
	}

	// 设置列宽
	for i := 0; i < len(headers); i++ {
		col := string(rune('A' + i))
		f.SetColWidth(sheet, col, col, 20)
	}

	// 写入表头
	for i, header := range headers {
		cell := fmt.Sprintf("%c1", 'A'+i)
		f.SetCellValue(sheet, cell, header)
	}

	// 写入数据
	for i, item := range data {
		row := i + 2
		f.SetCellValue(sheet, fmt.Sprintf("A%d", row), item["product_id"])
		f.SetCellValue(sheet, fmt.Sprintf("B%d", row), item["cargo_num"])
		f.SetCellValue(sheet, fmt.Sprintf("C%d", row), item["product_name"])
		f.SetCellValue(sheet, fmt.Sprintf("D%d", row), item["package_unit"])
		f.SetCellValue(sheet, fmt.Sprintf("E%d", row), item["spec"])
		f.SetCellValue(sheet, fmt.Sprintf("F%d", row), item["delivery_cycle"])
		f.SetCellValue(sheet, fmt.Sprintf("G%d", row), item["list_price"])
		f.SetCellValue(sheet, fmt.Sprintf("H%d", row), item["unit_price"])
		f.SetCellValue(sheet, fmt.Sprintf("I%d", row), item["brand"])
		f.SetCellValue(sheet, fmt.Sprintf("J%d", row), item["category"])
		f.SetCellValue(sheet, fmt.Sprintf("K%d", row), item["description"])
		f.SetCellValue(sheet, fmt.Sprintf("L%d", row), item["storage_condition"])
		f.SetCellValue(sheet, fmt.Sprintf("M%d", row), item["purity"])
		f.SetCellValue(sheet, fmt.Sprintf("N%d", row), item["status"])
		f.SetCellValue(sheet, fmt.Sprintf("O%d", row), item["cas_no"])
		f.SetCellValue(sheet, fmt.Sprintf("P%d", row), item["tips"])
	}

	// 保存文件
	current_date := time.Now().Format("20060102")
	start_index := (batchNum-1)*BatchSize + 1
	end_index := batchNum * BatchSize
	filename := filepath.Join(ExportDir, fmt.Sprintf("products_%s_%d_%d.xlsx", current_date, start_index, end_index))

	if err := f.SaveAs(filename); err != nil {
		return "", fmt.Errorf("failed to save excel file: %v", err)
	}

	return filename, nil
}

// ExportItems 导出所有商品数据
func (t *ItemExportTask) ExportItems(workerCount int) ([]string, error) {
	// Get CPU count if worker count not specified
	if workerCount <= 0 {
		workerCount = runtime.NumCPU()
	}

	// Get items to export
	filterDate := time.Date(2024, 11, 26, 0, 0, 0, 0, time.UTC)
	var items []ItemDBModel
	if err := t.db.Table("prod_items").Where("updated_at >= ?", filterDate).Find(&items).Error; err != nil {
		return nil, fmt.Errorf("failed to fetch items: %v", err)
	}

	// Create channels for work distribution and results
	type workItem struct {
		batchNum int
		items    []ItemDBModel
	}

	type result struct {
		filename string
		err      error
	}

	workChan := make(chan workItem)
	resultChan := make(chan result)

	// Use WaitGroup to track workers
	var wg sync.WaitGroup

	// Start worker pool
	for i := 0; i < workerCount; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for work := range workChan {
				// Process batch
				transformedData := t.transformData(work.items)
				filename, err := t.exportBatch(transformedData, work.batchNum)

				// Send result
				resultChan <- result{
					filename: filename,
					err:      err,
				}
			}
		}()
	}

	// Start goroutine to close result channel when all workers done
	go func() {
		wg.Wait()
		close(resultChan)
	}()

	// Distribute work
	go func() {
		for i := 0; i < len(items); i += BatchSize {
			end := i + BatchSize
			if end > len(items) {
				end = len(items)
			}

			workChan <- workItem{
				batchNum: i/BatchSize + 1,
				items:    items[i:end],
			}
		}
		close(workChan)
	}()

	// Collect results
	var exportedFiles []string
	var exportErrors []error

	for r := range resultChan {
		if r.err != nil {
			exportErrors = append(exportErrors, r.err)
			t.logger.Errorf("Failed to export batch: %v", r.err)
			continue
		}
		if r.filename != "" {
			exportedFiles = append(exportedFiles, r.filename)
			t.logger.Infof("Successfully exported to %s", r.filename)
		}
	}

	// Check if any exports failed
	if len(exportErrors) > 0 {
		return exportedFiles, fmt.Errorf("some exports failed: %v", exportErrors[0])
	}

	return exportedFiles, nil
}

// Helper functions
func truncateString(s string, maxLen int) string {
	if len(s) > maxLen {
		return s[:maxLen]
	}
	return s
}

func initDeliveryMap() map[string]string {
	return map[string]string{
		"货期咨询":    "",
		"半年以上":    "",
		"5-6个月":   "",
		"4-5个月":   "",
		"12-16周":  "",
		"8-12周":   "",
		"6-8周":    "",
		"4-6周":    "",
		"3-4周":    "3-4周",
		"2-3周":    "3-4周",
		"1-2周":    "1-2周",
		"5-7个工作日": "1周",
		"3-5个工作日": "3-5天",
		"1-2个工作日": "1-2天",
		"现货":      "现货",
	}
}

func initBrandMap() map[string]string {
	return map[string]string{
		"macklin": "Macklin(麦克林)",
		"麦克林":     "Macklin(麦克林)",
		"阿拉丁":     "Aladdin(阿拉丁)",
		"毕得医药":    "毕得",
		"罗恩":      "罗恩",
	}
}

// ExportItemsTask 可以被外部调用的导出任务函数
func ExportItemsTask(channelCode string, dbConfig DBConfig, workerCount int) map[string]interface{} {
	task, err := NewItemExportTask(dbConfig, channelCode)
	if err != nil {
		return map[string]interface{}{
			"status":  "error",
			"message": err.Error(),
		}
	}

	exportedFiles, err := task.ExportItems(workerCount)
	if err != nil {
		return map[string]interface{}{
			"status":  "error",
			"message": err.Error(),
		}
	}

	return map[string]interface{}{
		"status":         "success",
		"message":        "商品数据导出完成",
		"exported_files": exportedFiles,
	}
}

// 添加表名方法
func (ItemDBModel) TableName() string {
	return "prod_items"
}

func (ExcelItemDBModel) TableName() string {
	return "prod_excel_items"
}
