<template>
        <div v-if="isList&&totalListGoal.length!==0">
            <list_paginated
                v-bind:list='listGoal'
                v-bind:title='titleGoal'
                v-bind:deleteItem="delItFundGoal"
                v-if="listGoal.length !== 0"/>
        </div>
</template>

<script>
    import axios from 'axios';
    import List_paginated from '../components/List_paginated';

    export default {
        name: 'Delete_goal',
        components: {'List_paginated': List_paginated},
        data() {
            return {
                isList: true,
                list_sharedGoal: [],
                listGoal: [],
                titleGoal: "Financial Goal",
                errors: [],
                fund_id: null,
                id: 0
            }
        },
        computed: {
            totalListGoal: function () {
                {
                    let result = this.listGoal;
                    for (var i = 0; i < this.list_sharedGoal.length; i++) {
                        result.push({
                            'id': this.list_sharedGoal[i].id_fund,
                            'name': this.list_sharedGoal[i].name_fund + ' / ' + this.list_sharedGoal[i].group_name
                        });
                    }
                    ;
                    return result
                }
            }
        },
        methods: {
            getData() {
                axios({
                    method: 'get',
                    url: '/api/v1/fund/show_goal/'
                })
                    .then(response => {
                        this.listGoal = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
                axios({
                    method: 'get',
                    url: '/api/v1/fund/show_goal_by_group/'
                })
                    .then(response => {
                        this.list_sharedGoal = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
            },
            delItFundGoal(fundId) {
                axios({
                    method: 'delete',
                    url: '/api/v1/fund/delete_fund_goal_category/' + fundId,
                }).then(response => {
                    this.reply = response.data;
                    alert(this.reply);
                    this.getData();
                }).catch(error => {
                    alert(error.response.data)
                })
            }
        },
        created() {
            this.getData();
        }
    }


</script>

<style scoped>

</style>

