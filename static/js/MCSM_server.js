function sendGetRequestAndReloadPage(apiUrl) {
    // 发起 GET 请求
    fetch(apiUrl, {
      method: 'GET'
    })
    .then(response => {
      if (response.ok) {
        // 请求成功后刷新页面
        location.reload();
      } else {
        console.error('请求失败');
      }
    })
    .catch(error => {
      console.error('发生错误:', error);
    });
  }
  
  // 调用该函数并传入 API 地址
//   sendGetRequestAndReloadPage('your_api_url');
  