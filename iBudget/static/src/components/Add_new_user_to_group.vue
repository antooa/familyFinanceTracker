<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            Add User
        </b-button>
        <b-modal ref="myModalRef2" hide-footer title="Add New User To Group">
            <div class="d-block text-center">
                <b-card>
                    <p class="card-text">
                        <b>User's Email</b>
                        <input type="email" v-model="email">
                        <br/>
                        <b>Admin </b>
                        <input type="checkbox" id="one" value="Admin" v-model="is_admin">
                        <br/>
                    </p>
                    <b-btn class="mt-3" variant="outline-primary" block @click="saveData" aria-disabled="true">Save</b-btn>
                    <b-btn class="mt-3" variant="outline-danger" block @click="hideModal">Close</b-btn>
                </b-card>
            </div>
        </b-modal>
    </div>
</template>

<script>

    import axios from 'axios';

    export default {
        name: "new_user",
        data() {
            return {
                is_admin: false,
                email: null
            }
        },
        props: ["group_id", "getData"],
        methods: {
            showModal() {
                this.$refs.myModalRef2.show();
            },
            hideModal() {
                this.$refs.myModalRef2.hide();
                this.clearAll();
            },
            clearAll(){
                this.email = null;
                this.is_admin = false;
            },
            saveData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/group/add_new_users_to_group/',
                    data: {
                        'group_id': this.group_id,
                        'users_email': this.email,
                        'is_admin': this.is_admin
                    }
                }).then(response => {
                    this.getData();
                    this.hideModal();
                    this.clearAll();
                })
            },
        },
    }
</script>

<style scoped>
    .card-text {
        text-align: left;
        margin-left: 150px;
    }

    #acc {
        margin-right: 20px;
    }

    #profile-thumbnail {
        margin-right: 5px;
    }
</style>
