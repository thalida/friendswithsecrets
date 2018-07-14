<template>
  <div class="app-base">
    <Header />
    <router-view :key="$route.fullPath"/>
  </div>
</template>

<script>
import Header from './Header';

export default {
  name: 'Base',
  components: {
    Header,
  },
};
</script>

<style>
</style>
