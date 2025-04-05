const app = getApp()

// 基础请求方法
const request = (url, method, data) => {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${app.globalData.baseUrl}${url}`,
      method,
      data,
      header: {
        'content-type': 'application/json',
        'Authorization': wx.getStorageSync('token') || ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // 未授权，跳转到登录页
          wx.navigateTo({
            url: '/pages/login/login'
          })
          reject(new Error('未授权，请重新登录'))
        } else {
          reject(new Error(res.data.message || '请求失败'))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

// GET请求
const get = (url, params = {}) => {
  let queryString = ''
  if (Object.keys(params).length > 0) {
    queryString = '?' + Object.keys(params)
      .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
      .join('&')
  }
  return request(`${url}${queryString}`, 'GET')
}

// POST请求
const post = (url, data) => {
  return request(url, 'POST', data)
}

// PUT请求
const put = (url, data) => {
  return request(url, 'PUT', data)
}

// DELETE请求
const del = (url) => {
  return request(url, 'DELETE')
}

module.exports = {
  get,
  post,
  put,
  delete: del
} 