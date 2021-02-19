<template>
  <v-container>
    <v-card>
      <v-card-title>
        Lista de contatos agrupados
      </v-card-title>
      <v-data-table
        :loading="loadingEmails"
        :headers="headers"
        :items="items"
        :items-per-page="10"
      >
        <template v-slot:[`item.emails`]="{ item }">
          <v-container>
            <a
              type="email"
              :href="'mailto:' + email"
              v-for="(email, index) in item.emails"
              :key="index"
            >
              {{ email }}<br />
            </a>
          </v-container>
        </template>
      </v-data-table>
    </v-card>
    <v-snackbar v-model="snackbar.show" :timeout="3000">
      <div class="text-center">
        {{ snackbar.text }}
      </div>
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  name: "Home",
  data: () => {
    return {
      snackbar: { show: false, text: "" },
      loadingEmails: false,
      emailAddresses: [],
      headers: [
        { text: "Domínio", value: "domain" },
        { text: "E-mails", value: "emails" }
      ]
    };
  },
  computed: {
    items() {
      return !this.loadingEmails
        ? this.emailAddresses.reduce((acc, emailAddress) => {
            const domain = emailAddress.split("@")[1];

            if (!acc.some(item => domain === item.domain)) {
              const emails = this.emailAddresses.filter(
                value => value.split("@")[1] === domain
              );

              acc.push({
                domain,
                emails
              });
            }
            return acc;
          }, [])
        : [];
    }
  },
  mounted() {
    this.loadingEmails = true;
    this.$axios
      .get("/api/emails")
      .then(({ data }) => {
        this.loadingEmails = false;
        this.emailAddresses = data.emails;
        if (!this.emailAddresses.length) {
          this.snackbar = { text: "Nenhum contato encontrado", show: true };
        }
      })
      .catch(() => {
        this.loadingEmails = false;
        this.snackbar = {
          text: "Erro ao obter lista de contatos",
          show: true
        };
      });
  }
};
</script>
