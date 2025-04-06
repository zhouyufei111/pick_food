<template>
  <div class="calorie-records">
    <el-card v-loading="loading">
      <div slot="header" class="header-with-filter">
        <span>热量记录</span>
        <div class="date-filter">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="handleDateChange"
            :picker-options="pickerOptions"
          ></el-date-picker>
        </div>
      </div>
      <div v-if="records.length === 0" class="no-data">
        <el-empty description="暂无热量记录数据"></el-empty>
      </div>
      <el-table v-else :data="records" style="width: 100%">
        <el-table-column prop="record_date" label="日期"></el-table-column>
        <el-table-column prop="meal_type" label="餐次" :formatter="formatMealType"></el-table-column>
        <el-table-column prop="food_name" label="食物名称"></el-table-column>
        <el-table-column prop="calories" label="热量 (kcal)"></el-table-column>
        <el-table-column prop="protein" label="蛋白质 (g)"></el-table-column>
        <el-table-column prop="fat" label="脂肪 (g)"></el-table-column>
        <el-table-column prop="carbs" label="碳水 (g)"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CalorieRecords',
  props: {
    userId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      records: [],
      loading: false,
      dateRange: null,
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setMonth(start.getMonth() - 1)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setMonth(start.getMonth() - 3)
            picker.$emit('pick', [start, end])
          }
        }]
      }
    }
  },
  created() {
    this.fetchCalorieRecords()
  },
  methods: {
    async fetchCalorieRecords() {
      this.loading = true
      try {
        const params = {}
        if (this.dateRange && this.dateRange.length === 2) {
          params.start_date = this.formatDate(this.dateRange[0])
          params.end_date = this.formatDate(this.dateRange[1])
        }
        
        const response = await axios.get(`/users/${this.userId}/food_records`, { params })
        this.records = response.data
        
        // 处理食物名称显示
        this.records = this.records.map(record => {
          return {
            ...record,
            food_name: record.custom_food_name || (record.food_item ? record.food_item.name : '未知食物')
          }
        })
      } catch (error) {
        console.error('获取热量记录失败:', error)
        this.$message.error('获取热量记录失败')
        
        // 使用模拟数据
        this.records = [
          {
            record_date: '2023-05-01',
            meal_type: 'breakfast',
            food_name: '鸡蛋炒饭',
            calories: 450,
            protein: 25,
            fat: 15,
            carbs: 60
          },
          {
            record_date: '2023-05-01',
            meal_type: 'lunch',
            food_name: '牛肉面',
            calories: 650,
            protein: 35,
            fat: 20,
            carbs: 80
          }
        ]
      } finally {
        this.loading = false
      }
    },
    formatDate(date) {
      const d = new Date(date)
      let month = '' + (d.getMonth() + 1)
      let day = '' + d.getDate()
      const year = d.getFullYear()
      
      if (month.length < 2) month = '0' + month
      if (day.length < 2) day = '0' + day
      
      return [year, month, day].join('-')
    },
    handleDateChange() {
      this.fetchCalorieRecords()
    },
    formatMealType(row) {
      const mealTypeMap = {
        'breakfast': '早餐',
        'lunch': '午餐',
        'dinner': '晚餐',
        'snack': '零食'
      }
      return mealTypeMap[row.meal_type] || row.meal_type
    }
  }
}
</script>

<style scoped>
.header-with-filter {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.date-filter {
  margin-left: 20px;
}
.no-data {
  padding: 20px 0;
  text-align: center;
}
</style> 