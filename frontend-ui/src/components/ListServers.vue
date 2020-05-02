<template>
  <div class="servers-list-component">
    {{ msg }}
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ListServersComponent',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:8000/get_servers';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
