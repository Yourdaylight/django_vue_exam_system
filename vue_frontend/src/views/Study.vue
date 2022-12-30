<template>

  <div>
    <!--  左边的树状结构-->
    <div class="custom-tree-container">
      <div class="block">
        <a @click="tableVisible"
           style="cursor: pointer;
                  font-weight: bold;
                  text-decoration: underline">
          章节目录(推荐列表)
        </a>
        <el-tree
            :data="data"
            show-checkbox
            node-key="id"
            default-expand-all
            :expand-on-click-node="false"
            :render-content="renderContent"
            style="margin-top: 10px"
        >
        </el-tree>
        <el-button type="primary" @click="saveContent">保存</el-button>
      </div>
    </div>

    <!--  右边的对应内容-->
    <div class="content" v-if="!showTable">
      <h2>
        {{ currentName }}
      </h2>
      <span>学习次数:{{ currentStudyTimes }}</span>
      <br>
      <span>最近完成学习时间:{{ lastStudyTime }}</span>
      <br>
      <textarea v-model="currentContent" cols=120 rows=40>
      </textarea>
      <el-button type="primary" @click="updateStudyRecord">完成学习</el-button>
    </div>
    <!--  表格框，这个显示的时候上面的div消失  -->
    <div class="content" v-if="showTable">
      <h3>推荐学习</h3>
      <el-table
          :data="tableData"
          style="width: 100%">
        <el-table-column
            prop="label"
            label="章节名称"
            width="180">
        </el-table-column>
        <el-table-column
            prop="study_times"
            label="学习次数">
        </el-table-column>
        <el-table-column
            prop="study_time"
            label="最近学习时间">
        </el-table-column>
        <el-table-column
            label="操作">
          <template slot-scope="scope">
            <el-button
                size="mini"
                @click="getLearnContentById(scope.row)">查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!--   弹窗输入框 -->
    <el-dialog :title="currentName" :visible.sync="dialogVisible">
      <el-form :model="form" label-width="80px">
        <el-form-item label="章节名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="章节内容" prop="content">
          <el-input type="textarea" v-model="form.content"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveContent">确 定</el-button>
      </span>
    </el-dialog>
  </div>


</template>

<script>


export default {
  data() {
    return {
      max_id: 9999,
      data: [],
      dialogVisible: false,
      currentContent: '',
      currentName: '',
      currentId: '',
      currentStudyTimes: 0,
      lastStudyTime: '',
      form: {
        name: '',
        content: ''
      },
      showTable: true,
      tableData: []
    }
  },

  //界面创建时请求接口获取目录树
  created() {
    this.getTree();
  },
  methods: {
    //修改showTable状态
    tableVisible() {
      this.showTable = !this.showTable;
    },
    getTree() {
      //获取章节目录树
      this.$axios({
        method: 'get',
        url: 'api/content/?student_id=' + this.$store.state.student.id
      }).then((res) => {
        this.data = res.data.data.tree;
        this.tableData = res.data.data.table;
      })
    },

    //点击目录树的节点时，获取对应的内容
    getLearnContentById(nodeData) {
      this.currentName = nodeData.label;
      this.currentId = nodeData.id;
      this.$axios({
        method: 'get',
        url: 'api/learn/?id=' + nodeData.id + '&student_id=' + this.$store.state.student.id
      }).then((res) => {
        console.log("get的返回值", res.data)
        this.showTable = false;
        this.currentContent = res.data.data.desc
        this.currentStudyTimes = res.data.data["study_times"]
        this.lastStudyTime = res.data.data["study_time"]
      })
    },
    //点击保存按钮后，更新学习记录
    updateStudyRecord() {
      let student = this.$store.state.student

      this.$axios({
        method: 'post',
        url: 'api/learn/',
        data: {
          study_id: this.currentId,
          student_id: student.id,
        }
      }).then((res) => {
        console.log("post的返回值", res.data)
      })
    },

    //保存内容
    saveContent() {
      this.$axios({
        method: 'post',
        url: 'api/content/',
        data: {
          content: this.data,
          desc: this.form.content,
          name: this.form.name,
          _id: this.currentId
        }
      }).then((res) => {
        this.$message({
          message: '保存成功',
          type: 'success'
        });
        this.dialogVisible = false;
        this.getTree()
      })
    },
    //添加节点目录
    append(data) {
      this.max_id += 1;
      const newChild = {id: this.max_id, label: "新的章节", children: []};
      if (!data.children) {
        this.$set(data, 'children', []);
      }
      data.children.push(newChild);
    },
    //删除节点目录
    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex(d => d.id === data.id);
      children.splice(index, 1);
    },

    changeVisible(nodeData) {
      this.currentName = nodeData.label;
      this.form.name = nodeData.label;
      this.form.content = this.currentContent
      this.currentId = nodeData.id;
      this.dialogVisible = !this.dialogVisible;
    },


    renderContent(h, {node, data, store}) {
      return (
          <span class="custom-tree-node">
            <span>
              <el-button type="text" on-click={() => this.getLearnContentById(node.data)}>{node.label}</el-button>
            </span>
            <span>
              <el-button size="mini" type="text" on-click={() => this.append(data)} icon="el-icon-plus"></el-button>
              <el-button size="mini" type="text" on-click={() => this.remove(node, data)} icon="el-icon-minus"></el-button>
              <el-button size="mini" type="text" on-click={() => this.changeVisible(node.data)} icon="el-icon-edit"></el-button>
            </span>
          </span>);
    }
  }
};
</script>

<style>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

.block {
  float: left;
}

.content {
  width: 70%;
  height: 100%;
  float: right;
  margin-right: 5%;
}

</style>
