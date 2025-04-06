<template>
  <div class="nutrition-goals">
    <el-card v-loading="loading">
      <div slot="header">
        <span>营养目标</span>
      </div>
      <div v-if="!hasProfile" class="no-data">
        <el-empty description="暂无营养目标数据"></el-empty>
      </div>
      <el-form v-else label-width="120px">
        <el-form-item label="身高">
          <span>{{ profile.height }} cm</span>
        </el-form-item>
        <el-form-item label="体重">
          <span>{{ profile.weight }} kg</span>
        </el-form-item>
        <el-form-item label="年龄">
          <span>{{ profile.age }} 岁</span>
        </el-form-item>
        <el-form-item label="性别">
          <span>{{ formatGender(profile.gender) }}</span>
        </el-form-item>
        <el-form-item label="活动水平">
          <span>{{ formatActivityLevel(profile.activity_level) }}</span>
        </el-form-item>
        <el-form-item label="基础代谢率">
          <span>{{ profile.bmr }} kcal</span>
        </el-form-item>
        <el-form-item label="每日热量目标">
          <span>{{ profile.calorie_target }} kcal</span>
        </el-form-item>
        <el-form-item label="蛋白质目标">
          <span>{{ profile.protein_target }} g</span>
        </el-form-item>
        <el-form-item label="脂肪目标">
          <span>{{ profile.fat_target }} g</span>
        </el-form-item>
        <el-form-item label="碳水目标">
          <span>{{ profile.carb_target }} g</span>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'NutritionGoals',
  props: {
    userId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      profile: {},
      loading: false,
      hasProfile: false
    }
  },
  created() {
    this.fetchNutritionGoals()
  },
  methods: {
    async fetchNutritionGoals() {
      this.loading = true
      try {
        const response = await axios.get(`/users/${this.userId}/profile`)
        this.profile = response.data.profile
        this.hasProfile = true
      } catch (error) {
        console.error('获取营养目标失败:', error)
        if (error.response && error.response.status === 404) {
          this.hasProfile = false
        } else {
          this.$message.error('获取营养目标失败')
          // 使用模拟数据
          this.profile = {
            height: 175,
            weight: 70,
            age: 30,
            gender: 'male',
            activity_level: 'moderate',
            bmr: 1700,
            calorie_target: 2000,
            protein_target: 100,
            fat_target: 70,
            carb_target: 250
          }
          this.hasProfile = true
        }
      } finally {
        this.loading = false
      }
    },
    formatGender(gender) {
      const genderMap = {
        'male': '男',
        'female': '女',
        'other': '其他'
      }
      return genderMap[gender] || gender
    },
    formatActivityLevel(level) {
      const levelMap = {
        'sedentary': '久坐不动',
        'light': '轻度活动',
        'moderate': '中度活动',
        'active': '活跃',
        'very_active': '非常活跃'
      }
      return levelMap[level] || level
    }
  }
}
</script>

<style scoped>
.no-data {
  padding: 20px 0;
  text-align: center;
}
</style> 