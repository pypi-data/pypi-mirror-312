<template>
  <v-autocomplete
    v-bind="$attrs"
    v-on="$listeners"
    hide-no-data
    :items="items"
    :item-text="(person) => `${person.fullName} (${person.shortName})`"
    item-value="id"
    :loading="loading"
  />
</template>

<script>
import queryMixin from "../../../mixins/queryMixin.js";
import { persons } from "./person.graphql";

export default {
  name: "PersonField",
  extends: "v-autocomplete",
  mixins: [queryMixin],
  props: {
    /**
     * The graphQL query used to retrieve the persons.
     */
    gqlQuery: {
      type: Object,
      required: false,
      default: () => persons,
    },
  },
};
</script>
