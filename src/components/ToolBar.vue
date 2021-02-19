<template>
  <v-app-bar app fixed dark color="indigo darken-2">
    <v-app-bar-nav-icon></v-app-bar-nav-icon>
    <v-app-bar-title>
      Super OrgContact -
      <small>Organização de Contatos</small>
    </v-app-bar-title>
    <v-spacer></v-spacer>

    <v-menu bottom min-width="200px" rounded offset-y>
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on">
          <v-avatar v-if="$store.getters.isSignedIn" color="teal" size="32">
            <img :src="user.photo" :alt="user.displayName" />
          </v-avatar>
        </v-btn>
      </template>
      <v-card>
        <v-list-item-content class="justify-center">
          <div class="mx-auto text-center">
            <v-avatar
              v-if="$store.getters.isSignedIn"
              color="teal"
              size="48"
              class="my-2"
            >
              <img :src="user.photo" :alt="user.displayName" />
            </v-avatar>
            <h3 class="my-2">{{ user.displayName }}</h3>
            <v-divider class="my-3"></v-divider>
            <v-btn
              v-if="$store.getters.isSignedIn"
              depressed
              rounded
              text
              @click="logout"
            >
              Sair
              <v-spacer></v-spacer>
              <v-icon x-small class="ml-2">mdi-logout</v-icon>
            </v-btn>
          </div>
        </v-list-item-content>
      </v-card>
    </v-menu>
  </v-app-bar>
</template>

<script>
export default {
  name: "ToolBar",
  methods: {
    logout() {
      this.$axios.get("/api/logout").then(() => {
        this.$store.dispatch("logout");
        this.$router.replace("/login");
      });
    }
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  }
};
</script>
