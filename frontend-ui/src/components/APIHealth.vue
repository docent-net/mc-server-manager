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
    };
  },
  methods: {
    getStatusMessage() {
      const path = 'http://localhost:8000/health';
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
    this.getStatusMessage();
  },
};
</script>
