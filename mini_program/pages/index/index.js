// pages/index/index.js
Page({
  data: {
    text: '',
    voices: [
      { id: 'zh_female_qingxin', name: '清新女声' },
      { id: 'zh_female_wenyi', name: '文艺女声' },
      { id: 'zh_female_chengshu', name: '成熟女声' },
      { id: 'zh_female_tianmei', name: '甜美女声' },
      { id: 'zh_male_qingxin', name: '清新男声' },
      { id: 'zh_male_wenyi', name: '文艺男声' },
      { id: 'zh_male_chengshu', name: '成熟男声' },
      { id: 'zh_male_tianmei', name: '甜美男声' }
    ],
    voiceIndex: 0,
    speed: 1.0,
    volume: 1.0,
    loading: false,
    audioUrl: ''
  },

  onInput(e) {
    this.setData({
      text: e.detail.value
    })
  },

  onVoiceChange(e) {
    this.setData({
      voiceIndex: e.detail.value
    })
  },

  onSpeedChange(e) {
    this.setData({
      speed: e.detail.value
    })
  },

  onVolumeChange(e) {
    this.setData({
      volume: e.detail.value
    })
  },

  generateTTS() {
    const { text, voices, voiceIndex, speed, volume } = this.data
    
    if (!text.trim()) {
      wx.showToast({
        title: '请输入文本',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    // 调用后端 API
    wx.request({
      url: 'https://你的域名/api/tts', // 替换为你的服务器域名
      method: 'POST',
      data: {
        text: text,
        voice: voices[voiceIndex].id,
        speed: speed,
        volume: volume
      },
      success: (res) => {
        if (res.data.success) {
          this.setData({
            audioUrl: res.data.audio_url
          })
          wx.showToast({
            title: '生成成功',
            icon: 'success'
          })
        } else {
          wx.showToast({
            title: res.data.message || '生成失败',
            icon: 'none'
          })
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        })
      },
      complete: () => {
        this.setData({ loading: false })
      }
    })
  },

  downloadAudio() {
    const { audioUrl } = this.data
    if (!audioUrl) return

    wx.downloadFile({
      url: audioUrl,
      success: (res) => {
        wx.saveFileToDisk({
          filePath: res.tempFilePath,
          success: () => {
            wx.showToast({
              title: '保存成功',
              icon: 'success'
            })
          }
        })
      }
    })
  }
})
