<script>
import AvatarContent from "../person/AvatarContent.vue";
import groupOverviewTabMixin from "../../mixins/groupOverviewTabMixin";
import SecondaryActionButton from "../generic/buttons/SecondaryActionButton.vue";
import itemsPerPageMixin from "../../mixins/itemsPerPageMixin.js";

export default {
  name: "GroupMembers",
  components: { AvatarContent, SecondaryActionButton },
  mixins: [groupOverviewTabMixin, itemsPerPageMixin],
  data() {
    return {
      headers: [
        {
          text: this.$t("person.avatar"),
          align: "start",
          sortable: false,
          value: "avatarContentUrl",
        },
        { text: this.$t("person.first_name"), value: "firstName" },
        { text: this.$t("person.last_name"), value: "lastName" },
        { text: this.$t("person.short_name"), value: "shortName" },
        { text: this.$t("person.birth_date"), value: "dateOfBirth" },
        { text: this.$t("person.sex.field"), value: "sex" },
        { text: this.$t("person.email_address"), value: "email" },
        { text: this.$t("person.username"), value: "username" },
        { align: "end", sortable: false, value: "id" },
      ],
    };
  },
};
</script>

<template>
  <v-data-table
    :headers="headers"
    :items="group.members"
    :items-per-page="itemsPerPage"
    :footer-props="footerProps"
  >
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.avatarContentUrl="{ item }">
      <v-avatar class="my-1">
        <avatar-content :image-url="item.avatarContentUrl" />
      </v-avatar>
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.shortName="{ item }">
      {{ item.shortName || "–" }}
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.sex="{ item }">
      {{ item.sex ? $t("person.sex." + item.sex.toLowerCase()) : "–" }}
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.dateOfBirth="{ item }">
      {{
        item.dateOfBirth ? $d($parseISODate(item.dateOfBirth), "short") : "–"
      }}
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.email="{ item }">
      <a v-if="item.email" :href="'mailto:' + item.email">{{ item.email }}</a>
      <span v-else>–</span>
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.username="{ item }">
      {{ item.username || "–" }}
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.id="{ item }">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <secondary-action-button
            v-bind="attrs"
            v-on="on"
            icon
            icon-text="mdi-open-in-new"
            :outlined="false"
            target="_blank"
            :to="{
              name: 'core.personById',
              params: {
                id: item.id,
              },
            }"
          >
          </secondary-action-button>
        </template>
        <span>{{ $t("person.view_in_new_tab", item) }}</span>
      </v-tooltip>
    </template>
  </v-data-table>
</template>

<style scoped></style>
