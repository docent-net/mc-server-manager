<template>
  <div class="servers-page">
    <ListServers msg="MC server manager"/>
    view test
  </div>
</template>

<script>
import ListServers from '@/components/ListServers.vue';

export default {
  name: 'ListServersView',
  components: {
    ListServers,
  },
};
</script>
