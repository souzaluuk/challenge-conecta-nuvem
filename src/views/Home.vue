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
  </v-container>
</template>

<script>
export default {
  name: "Home",
  data: () => {
    return {
      gapi: null,
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
            const domain = emailAddress.value.split("@")[1];
            if (!acc.some(item => domain === item.domain)) {
              const emails = this.emailAddresses
                .filter(({ value }) => value.split("@")[1] === domain)
                .map(({ value }) => value);
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
  methods: {
    listConnectionEmails(pageToken) {
      this.loadingEmails = true;

      this.gapi.client.people.people.connections
        .list({
          resourceName: "people/me",
          personFields: "names,emailAddresses",
          pageToken
        })
        .then(res => {
          this.emailAddresses = this.emailAddresses.concat(
            res.result.connections
              .filter(person => {
                return !!person.emailAddresses;
              })
              .reduce((acc, person) => {
                acc = acc.concat(person.emailAddresses);
                return acc;
              }, [])
          );
          if (res.result.nextPageToken) {
            this.listConnectionEmails(res.result.nextPageToken);
          } else {
            this.loadingEmails = false;
          }
        });
    }
  },
  mounted() {
    this.$gapi
      .getGapiClient()
      .then(gapi => {
        this.gapi = gapi;
      })
      .then(() => this.listConnectionEmails());
  }
};
</script>
