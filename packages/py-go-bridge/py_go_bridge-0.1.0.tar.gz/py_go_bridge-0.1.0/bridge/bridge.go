package main

// #include <stdlib.h>
import "C"
import (
	"encoding/json"
	"fmt"
	"pygo/pkg/export"
	"time"
	"unsafe"
)

// StandardResponse 标准响应结构
type StandardResponse struct {
	Status string      `json:"status"` // succeed/failed
	Code   int         `json:"code"`   // 200,400,500等
	Msg    string      `json:"msg"`    // 提示信息
	Data   interface{} `json:"data"`   // 实际数据
	Timing int64       `json:"timing"` // 执行耗时(毫秒)
}

// wrapGoFunction 包装Go函数调用
func wrapGoFunction(f func() (interface{}, error)) *C.char {
	start := time.Now()

	response := &StandardResponse{
		Status: "succeed",
		Code:   200,
		Msg:    "ok",
	}

	// 执行函数
	data, err := f()
	if err != nil {
		response.Status = "failed"
		response.Code = 500
		response.Msg = err.Error()
	} else {
		response.Data = data
	}

	// 计算耗时
	response.Timing = time.Since(start).Milliseconds()

	// 转JSON
	jsonResult, err := json.Marshal(response)
	if err != nil {
		// 如果JSON序列化失败,返回错误信息
		errResp := &StandardResponse{
			Status: "failed",
			Code:   500,
			Msg:    fmt.Sprintf("JSON marshal error: %v", err),
			Timing: time.Since(start).Milliseconds(),
		}
		jsonResult, _ = json.Marshal(errResp)
	}

	return C.CString(string(jsonResult))
}

//export ExportExcel
func ExportExcel(channelCode *C.char, host *C.char, port C.int, user *C.char, password *C.char, database *C.char, workerCount C.int) *C.char {
	return wrapGoFunction(func() (interface{}, error) {
		// 转换参数
		config := export.DBConfig{
			Host:     C.GoString(host),
			Port:     int(port),
			User:     C.GoString(user),
			Password: C.GoString(password),
			Database: C.GoString(database),
		}

		// 调用原始函数
		result := export.ExportItemsTask(C.GoString(channelCode), config, int(workerCount))

		// 这里可以处理错误,如果ExportItemsTask返回的result中包含错误信息
		if result["status"] == "error" {
			return nil, fmt.Errorf(result["message"].(string))
		}

		return result, nil
	})
}

//export NewFunction
func NewFunction(param1 *C.char, param2 C.int) *C.char {
	return wrapGoFunction(func() (interface{}, error) {
		// 示例函数实现
		data := map[string]interface{}{
			"param1": C.GoString(param1),
			"param2": int(param2),
		}
		return data, nil
	})
}

//export FreeString
func FreeString(str *C.char) {
	if str != nil {
		C.free(unsafe.Pointer(str))
	}
}

func main() {}
