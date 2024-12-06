/**
 * Vue mixin containing permission checking code.
 */

const permissionsMixin = {
  methods: {
    checkPermission(permissionName) {
      return (
        this.$root.permissions &&
        this.$root.permissions.find((p) => p.name === permissionName) &&
        this.$root.permissions.find((p) => p.name === permissionName).result
      );
    },
    addPermissions(newPermissionNames) {
      this.$root.permissionNames = [
        ...new Set([...this.$root.permissionNames, ...newPermissionNames]),
      ];
    },
  },
};

export default permissionsMixin;
