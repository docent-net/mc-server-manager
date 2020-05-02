<template>
  <div class="apihealth-page">
    <APIHealthComponent/>
  </div>
</template>

<script>
import APIHealthComponent from '@/components/APIHealth.vue';

export default {
  name: 'APIHealthView',
  components: {
    APIHealthComponent,
  },
};
</script>
