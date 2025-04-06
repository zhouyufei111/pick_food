<template>
  <div class="user-preferences">
    <el-card v-loading="loading">
      <div slot="header">
        <span>饮食偏好</span>
      </div>
      <div v-if="!hasPreferences" class="no-data">
        <el-empty description="暂无饮食偏好数据"></el-empty>
      </div>
      <el-form v-else label-width="120px">
        <el-form-item label="常吃食物">
          <el-tag v-for="(food, index) in preferences.frequentFoods" :key="'frequent-'+index" type="success" style="margin-right: 5px; margin-bottom: 5px">
            {{ food.name }} ({{ food.count }}次)
          </el-tag>
        </el-form-item>
        <el-form-item label="偏好餐厅">
          <el-tag v-for="(restaurant, index) in preferences.favoriteRestaurants" :key="'restaurant-'+index" type="info" style="margin-right: 5px; margin-bottom: 5px">
            {{ restaurant.name }} ({{ restaurant.count }}次)
          </el-tag>
        </el-form-item>
        <el-form-item label="餐次分布">
          <div class="chart-container" ref="mealTypeChart"></div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'UserPreferences',
  props: {
    userId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      preferences: {
        frequentFoods: [],
        favoriteRestaurants: [],
        mealTypeDistribution: {}
      },
      loading: false,
      hasPreferences: false,
      chart: null
    }
  },
  created() {
    this.fetchUserPreferences()
  },
  mounted() {
    this.$nextTick(() => {
      if (this.hasPreferences) {
        this.initChart()
      }
    })
  },
  methods: {
    async fetchUserPreferences() {
      this.loading = true
      try {
        // 这里应该从API获取数据
        // 由于目前没有专门的API，我们可以分析用户的食物记录来获取偏好
        // 或者使用模拟数据
        
        // 模拟数据
        this.preferences = {
          frequentFoods: [
            { name: '鸡胸肉', count: 15 },
            { name: '西兰花', count: 12 },
            { name: '糙米', count: 10 },
            { name: '鸡蛋', count: 8 },
            { name: '牛奶', count: 7 }
          ],
          favoriteRestaurants: [
            { name: '健康餐厅', count: 8 },
            { name: '沙拉专卖', count: 6 },
            { name: '营养快餐', count: 5 }
          ],
          mealTypeDistribution: {
            breakfast: 25,
            lunch: 30,
            dinner: 28,
            snack: 17
          }
        }
        this.hasPreferences = true
        
        this.$nextTick(() => {
          this.initChart()
        })
      } catch (error) {
        console.error('获取用户偏好失败:', error)
        this.hasPreferences = false
      } finally {
        this.loading = false
      }
    },
    initChart() {
      if (!this.$refs.mealTypeChart) return
      
      this.chart = echarts.init(this.$refs.mealTypeChart)
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'horizontal',
          bottom: 10,
          data: ['早餐', '午餐', '晚餐', '零食']
        },
        series: [
          {
            name: '餐次分布',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: this.preferences.mealTypeDistribution.breakfast, name: '早餐' },
              { value: this.preferences.mealTypeDistribution.lunch, name: '午餐' },
              { value: this.preferences.mealTypeDistribution.dinner, name: '晚餐' },
              { value: this.preferences.mealTypeDistribution.snack, name: '零食' }
            ]
          }
        ]
      }
      
      this.chart.setOption(option)
      
      window.addEventListener('resize', this.resizeChart)
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize()
      }
    }
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart)
    if (this.chart) {
      this.chart.dispose()
      this.chart = null
    }
  }
}
</script>

<style scoped>
.no-data {
  padding: 20px 0;
  text-align: center;
}
.chart-container {
  width: 100%;
  height: 300px;
}
</style> 