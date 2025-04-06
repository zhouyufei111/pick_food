<template>
  <div class="user-list">
    <h1>用户列表</h1>
    <div class="table-operations">
      <el-input
        v-model="searchQuery"
        placeholder="搜索用户"
        style="width: 200px"
        @input="handleSearch"
      >
        <i slot="prefix" class="el-icon-search"></i>
      </el-input>
    </div>
    
    <el-table :data="users" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="username" label="用户名"></el-table-column>
      <el-table-column prop="phone" label="手机号"></el-table-column>
      <el-table-column prop="nickname" label="微信昵称"></el-table-column>
      <el-table-column prop="created_at" label="创建时间"></el-table-column>
      <el-table-column label="操作" width="250">
        <template slot-scope="scope">
          <el-button 
            size="mini" 
            @click="handleView(scope.row)"
          >查看</el-button>
          <el-button 
            size="mini" 
            type="primary" 
            @click="handleEdit(scope.row)"
          >编辑</el-button>
          <el-button 
            size="mini" 
            type="danger" 
            @click="handleDelete(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserList',
  data() {
    return {
      users: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      total: 0,
      loading: false
    }
  },
  created() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await axios.get('/users/list', {
          params: {
            page: this.currentPage,
            per_page: this.pageSize,
            search: this.searchQuery
          }
        })
        
        this.users = response.data.items
        this.total = response.data.total
      } catch (error) {
        console.error('获取用户列表失败:', error)
        this.$message.error('获取用户列表失败')
        
        // 使用模拟数据作为备用
        this.users = [
          {
            id: 1,
            username: '测试用户1',
            phone: '13800138001',
            created_at: '2023-01-01'
          },
          {
            id: 2,
            username: '测试用户2',
            phone: '13800138002',
            created_at: '2023-01-02'
          }
        ]
        this.total = 2
      } finally {
        this.loading = false
      }
    },
    handleView(row) {
      this.$router.push(`/users/${row.id}`)
    },
    async handleEdit(row) {
      this.$router.push(`/users/${row.id}/edit`)
    },
    async handleDelete(row) {
      this.$confirm('确认删除该用户?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await axios.delete(`/users/${row.id}`)
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.fetchUsers()
        } catch (error) {
          console.error('删除用户失败:', error)
          this.$message.error('删除用户失败')
        }
      }).catch(() => {})
    },
    handleSearch() {
      this.currentPage = 1
      this.fetchUsers()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.fetchUsers()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchUsers()
    }
  }
}
</script>

<style scoped>
.table-operations {
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 