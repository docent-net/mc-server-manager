<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Servers list</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Create new server</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Server name</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(server, index) in servers" :key="index">
              <td>{{ server.server_name }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Activate</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ListServersComponent',
  data() {
    return {
      servers: '',
    };
  },
  methods: {
    getServers() {
      const path = 'http://localhost:8000/get_servers';
      axios.get(path)
        .then((res) => {
          this.servers = res.data.servers;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getServers();
  },
};
</script>
