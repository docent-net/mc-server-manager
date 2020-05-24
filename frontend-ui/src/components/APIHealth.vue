<template>
  <div class="apihealth-component">
  <button type="button" class="btn btn-primary">API health: {{ msg.status }}</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'APIHealthComponent',
  data() {
    return {
      msg: '',
      APIAddr: '',
    };
  },
  methods: {
    getStatusMessage() {
      const path = `${this.APIAddr}/health`;
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    setAPIServerAddr() {
      this.APIAddr = process.env.VUE_APP_API_ADDR;
    },
  },
  created() {
    this.setAPIServerAddr();
    this.getStatusMessage();
  },
};
</script>
