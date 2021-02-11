<template>
  <v-container style="height: 400px;">
    <v-row class="fill-height" align-content="center" justify="center">
      <v-col class="subtitle-1 text-center" cols="12"></v-col>
      <v-col cols="6">
        <v-progress-linear
          color="indigo accent-4"
          indeterminate
          rounded
          height="6"
        ></v-progress-linear>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Loading"
};
</script>

<style></style>
