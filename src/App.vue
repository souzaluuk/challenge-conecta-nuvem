<template>
  <v-app>
    <ToolBar v-if="!loginPageIsActive" />
    <v-main>
      <router-view v-if="loginPageIsActive" />
      <Loading v-else-if="loading" />
      <router-view v-else />
    </v-main>
  </v-app>
</template>

<script>
import ToolBar from "./components/ToolBar";
import Loading from "./components/LoadingPage";

export default {
  name: "App",
  components: { ToolBar, Loading },
  methods: {
    setSignedIn(isSignedIn) {
      if (isSignedIn) {
        this.$store.dispatch("login");
        if (this.loginPageIsActive) {
          this.$router.replace("/");
        }
      } else {
        this.$store.dispatch("logout");
        if (!this.loginPageIsActive) {
          this.$router.replace("/login");
        }
      }
    }
  },
  computed: {
    loginPageIsActive() {
      return this.$route.name === "Login";
    },
    loading() {
      return this.$store.state.loading;
    }
  },
  mounted() {
    this.$gapi.getGapiClient().then(gapi => {
      gapi.auth2.getAuthInstance().isSignedIn.listen(this.setSignedIn);
      this.setSignedIn(gapi.auth2.getAuthInstance().isSignedIn.get());
    });
  }
};
</script>
