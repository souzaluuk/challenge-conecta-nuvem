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
    setLoading(loading) {
      this.$store.dispatch("setLoading", loading);
    },
    login(user) {
      this.$store.dispatch("login", user);
      if (this.loginPageIsActive) {
        this.$router.replace("/");
      }
    },
    logout() {
      this.$store.dispatch("logout");
      if (!this.loginPageIsActive) {
        this.$router.replace("/login");
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
    this.setLoading(true);
    this.$axios
      .post("/api/login")
      .then(({ data }) => {
        this.login(data);
        this.setLoading(false);
      })
      .catch(() => {
        this.logout();
        this.setLoading(false);
      });
  }
};
</script>

<style>
html {
  overflow-y: auto;
}
</style>
