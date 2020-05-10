<!-- eslint-disable max-len, no-trailing-spaces -->
<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <alert :message="message" v-if="showMessage"></alert>
        <div class="btn-group" role="group">
        <button type="button" class="btn btn-success btn-sm" v-b-modal.server-modal>Create</button>
        <button type="button" class="btn btn-warning btn-sm" v-b-modal.restart-modal>
        Restart {{ activeServer }}
        </button>
        </div>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Currently active server: {{ activeServer }}</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(server, index) in servers" :key="index">
              <td>{{ server.server_name }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button v-b-modal.activate-modal 
                    @click="setActivationServer(server.server_name)" 
                    v-if="server.server_name != activeServer" 
                    type="button" 
                    class="btn btn-warning btn-sm">
                    Activate
                  </button>
                  <button v-b-modal.delete-modal type="button" 
                    @click="setDeleteServer(server.server_name)" 
                    class="btn btn-danger btn-sm" 
                    v-if="(server.server_secured != true) && (activeServer != server.server_name)">
                    Delete
                  </button>
                  <button v-b-modal.secure-modal 
                    @click="setSecureServer(server.server_name)" 
                    v-if="server.server_secured != true" 
                    type="button" 
                    class="btn btn-warning btn-sm">
                    Secure
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="createServerModal"
          id="server-modal"
          title="Create a new server"
          hide-footer>
    <b-form @submit="onCreateServerSubmit" @reset="onCreateServerReset" class="w-100">
    <b-form-group id="form-title-group"
                  label="Name (max 32 chars, only alphanumeric, hyphen, underscore):"
                  label-for="form-title-input">
        <b-form-input id="form-title-input"
                      type="text"
                      v-model="createServerForm.serverName"
                      required
                      placeholder="server name">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-activate-group">
        <b-form-checkbox-group v-model="createServerForm.activateOnCreation" id="form-checks">
          <b-form-checkbox value="true">Activate?</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>
      <b-button type="submit" variant="primary">Create</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </b-modal>
  <b-modal ref="restartServerModal"
          id="restart-modal"
          title="Restart server"
          hide-footer>
    <p>This will restart server {{ activeServer }}. 
      Game will be unavailable for a while.</p>
    <b-form @submit="onRestartServerSubmit" class="w-100">
      <b-button type="submit" variant="primary">Restart {{ activeServer }}</b-button>
      <b-button type="button" @click="closeRestartServerModal" variant="danger">Cancel</b-button>
    </b-form>
  </b-modal>
  <b-modal ref="activateServerModal"
          id="activate-modal"
          title="Activate server"
          hide-footer>
    <p>This will stop the current server (<b>{{ activeServer}}</b>), make 
      the server <b>{{ activationServerName }}</b> active and start it.
    </p>
    <b-form @submit="onActivateServerSubmit" class="w-100">
      <b-button type="submit" variant="primary">Activate {{ activationServerName }}</b-button>
      <b-button type="button" @click="closeActivateServerModal" variant="danger">Cancel</b-button>
    </b-form>
  </b-modal>
  <b-modal ref="secureServerModal"
          id="secure-modal"
          title="Secure server"
          hide-footer>
    <p>This will secure the server {{ secureServerName }}. 
      You will not be able to delete this server from server manager.
      You will need to remove this server data manually from the filesystem.
    </p>
    <p>In case you'd like to remove this security lock you will need to
      delete <b>.mc-server-manager-secure.lock</b> file from the server
      data directory.</p>
    <b-form @submit="onSecureServerSubmit" class="w-100">
      <b-button type="submit" variant="primary">Secure {{ secureServerName }}</b-button>
      <b-button type="button" @click="closeSecureServerModal" variant="danger">Cancel</b-button>
    </b-form>
  </b-modal>
  <b-modal ref="deleteServerModal"
          id="delete-modal"
          title="Delete server"
          hide-footer>
    <p>This will completely delete server <b>{{ deleteServerName }}</b>!</p>
    <p>All data of this server will be lost!</p>
    <b-form @submit="onDeleteServerSubmit" class="w-100">
      <b-button type="submit" variant="primary">Delete {{ deleteServerName }}</b-button>
      <b-button type="button" @click="closeDeleteServerModal" variant="danger">Cancel</b-button>
    </b-form>
  </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import InfoBox from './InfoBox.vue';

export default {
  name: 'ListServersComponent',
  data() {
    return {
      servers: '',
      activeServer: '',
      activationServerName: '',
      secureServerName: '',
      deleteServerName: '',
      createServerForm: {
        serverName: '',
        activateOnCreation: [],
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: InfoBox,
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
    createServer(payload) {
      const path = 'http://localhost:8000/create_server';
      axios.put(path, payload)
        .then(() => {
          this.getServers();
          this.message = 'Server created!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.message = error;
          this.getServers();
        });
      this.showMessage = true;
      this.activeServer = payload.server_name;
    },
    initCreateServerForm() {
      this.createServerForm.serverName = '';
      this.createServerForm.activateOnCreation = [];
    },
    onCreateServerSubmit(evt) {
      evt.preventDefault();
      this.$refs.createServerModal.hide();
      let activateOnCreation = false;
      if (this.createServerForm.activateOnCreation[0]) activateOnCreation = true;
      const payload = {
        server_name: this.createServerForm.serverName,
        activate: activateOnCreation, // property shorthand
      };
      this.createServer(payload);
      this.initCreateServerForm();
    },
    onCreateServerReset(evt) {
      evt.preventDefault();
      this.$refs.restartServerModal.hide();
      this.initCreateServerForm();
      this.showMessage = false;
    },
    restartServer() {
      const path = 'http://localhost:8000/restart_server';
      axios.get(path)
        .then(() => {
          this.getServers();
          this.message = 'Server restarted!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.message = error;
          this.getServers();
        });
      this.showMessage = true;
    },
    onRestartServerSubmit(evt) {
      evt.preventDefault();
      this.$refs.restartServerModal.hide();
      this.restartServer();
    },
    closeRestartServerModal() {
      this.$refs.restartServerModal.hide();
    },
    getActiveServer() {
      const path = 'http://localhost:8000/get_active_server';
      axios
        .get(path)
        // eslint-disable-next-line arrow-parens
        .then(response => {
          this.activeServer = response.data.activeServer;
        });
    },
    activateServer() {
      const payload = {
        server_name: this.activationServerName,
      };
      const path = 'http://localhost:8000/activate_server';
      axios.post(path, payload)
        .then(() => {
          this.activeServer = this.activationServerName;
          this.getServers();
          this.message = 'Server activated!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.message = error;
          this.getServers();
        });
      this.showMessage = true;
    },
    setActivationServer(serverName) {
      this.activationServerName = serverName;
    },
    onActivateServerSubmit(evt) {
      evt.preventDefault();
      this.$refs.activateServerModal.hide();
      this.activateServer();
    },
    closeActivateServerModal() {
      this.$refs.activateServerModal.hide();
    },
    secureServer() {
      const payload = {
        server_name: this.secureServerName,
      };
      const path = 'http://localhost:8000/secure_server_instance';
      axios.post(path, payload)
        .then(() => {
          this.getServers();
          this.message = 'Server secured!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.message = error;
          this.getServers();
        });
      this.showMessage = true;
    },
    setSecureServer(serverName) {
      this.secureServerName = serverName;
    },
    onSecureServerSubmit(evt) {
      evt.preventDefault();
      this.$refs.secureServerModal.hide();
      this.secureServer();
    },
    closeSecureServerModal() {
      this.$refs.secureServerModal.hide();
    },
    deleteServer() {
      const path = `http://localhost:8000/delete_server_instance/${this.deleteServerName}`;
      axios.delete(path)
        .then(() => {
          this.getServers();
          this.message = 'Server deleted!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.message = error;
          this.getServers();
        });
      this.showMessage = true;
    },
    setDeleteServer(serverName) {
      this.deleteServerName = serverName;
    },
    onDeleteServerSubmit(evt) {
      evt.preventDefault();
      this.$refs.deleteServerModal.hide();
      this.deleteServer();
    },
    closeDeleteServerModal() {
      this.$refs.deleteServerModal.hide();
    },
  },
  created() {
    this.getActiveServer();
    this.getServers();
  },
};
</script>
