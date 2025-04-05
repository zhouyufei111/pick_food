// app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    
    // 在全局数据设置完成后，再引入用户服务并执行登录
    setTimeout(() => {
      const userService = require('./services/user.js');
      
      // 检查登录状态，如果未登录则执行登录
      if (!userService.checkLoginStatus()) {
        userService.login()
          .then(res => {
            console.log('登录成功', res);
          })
          .catch(err => {
            console.error('登录失败', err);
          });
      }
    }, 0);
  },
  globalData: {
    userInfo: null,
    baseUrl: 'http://localhost:4000/api',  // 修改为你的实际后端地址
    // 默认营养目标
    nutritionGoals: {
      calories: 2000,
      protein: 125,
      fat: 83,
      carbs: 313
    }
  }
}) 