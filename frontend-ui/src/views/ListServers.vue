<template>
  <div class="servers-page">
    <ListServersComponent/>
  </div>
</template>

<script>
import ListServersComponent from '@/components/ListServers.vue';

export default {
  name: 'ListServersView',
  components: {
    ListServersComponent,
  },
};
</script>
