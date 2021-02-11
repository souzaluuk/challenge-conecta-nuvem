<template>
  <v-container fill-height>
    <v-card
      :loading="loading"
      :disabled="loading"
      class="mx-auto text-center"
      max-width="300px"
    >
      <h3 class="my-4">
        Super OrgContact
        <br />
        <small>
          Organização de Contatos
        </small>
      </h3>
      <v-icon size="70px" class="my-3">
        mdi-account-circle
      </v-icon>
      <v-card-text>
        Você precisa realizar o login com a conta do Google para utilizar a
        aplicação.<br />
        Clique em <code>Login</code> e autorize a solicitação de uso
      </v-card-text>
      <v-btn
        v-if="isSignedIn"
        class="my-3"
        text
        color="indigo accent-4"
        @click="logout"
      >
        Logout
      </v-btn>
      <v-btn v-else class="my-4" text color="indigo accent-4" @click="login">
        Login
      </v-btn>
    </v-card>
  </v-container>
</template>
<script>
export default {
  name: "Login",
  data: () => {
    return { gapi: null };
  },
  methods: {
    login() {
      this.setLoading(true);
      this.gapi.auth2
        .getAuthInstance()
        .signIn()
        .catch(() => this.setLoading(false));
    },
    logout() {
      this.setLoading(true);
      this.gapi.auth2
        .getAuthInstance()
        .signOut()
        .catch(() => {
          this.setLoading(false);
        });
    },
    setLoading(loading) {
      this.$store.dispatch("setLoading", loading);
    }
  },
  computed: {
    isSignedIn() {
      return this.$store.state.isSignedIn;
    },
    loading() {
      return this.$store.state.loading;
    }
  },
  mounted() {
    this.$gapi.getGapiClient().then(gapi => {
      this.gapi = gapi;
    });
  }
};
</script>
