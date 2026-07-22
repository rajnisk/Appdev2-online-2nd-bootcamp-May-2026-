<template>
  <h1> {{ message }} </h1>
  <input type="text" v-model="message" />
  <div v-for="student in studentData">
    <p>name: {{ student.name }}</p>
    <p>age: {{ student.age }}</p>

  </div>
  <button type="button" class="btn btn-danger">Primary</button>

</template>

<script>
import axios from 'axios';

export default {
  name: 'HomeView',
  data() {
    return {
      message: 'Hello World',
      studentData: []
    }
  },
    methods: {
    async hello(){
      const resp = await axios.get('http://127.0.0.1:5000/')
      console.log(resp)
      this.studentData = resp.data.student_data
    }
  },
  mounted(){
    this.hello()
  }

}
</script>