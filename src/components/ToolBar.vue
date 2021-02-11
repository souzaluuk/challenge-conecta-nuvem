<template>
  <v-app-bar app absolute dark color="indigo darken-2">
    <v-container>
      <v-row>
        <v-app-bar-title>
          <v-icon>mdi-contacts</v-icon>
          Super OrgContact -
          <small>Organização de Contatos</small>
        </v-app-bar-title>
        <v-spacer></v-spacer>
        <v-btn v-if="$store.state.isSignedIn" text right @click="logout">
          Sair
          <v-icon small>mdi-logout</v-icon>
        </v-btn>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  name: "ToolBar",
  methods: {
    logout() {
      this.setLoading(true);
      this.$gapi.getGapiClient().then(gapi => {
        gapi.auth2
          .getAuthInstance()
          .signOut()
          .catch(() => {
            this.setLoading(false);
          });
      });
    },
    setLoading(loading) {
      this.$store.dispatch("setLoading", loading);
    }
  }
};
</script>
