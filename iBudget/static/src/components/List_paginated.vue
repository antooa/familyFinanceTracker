<template>
    <div class="content">
        <div class="paginated-list">
            <ul class="list-group">
                <li
                    class="list-group-item list-group-item-action pointer"
                    v-for="(item, index) in paginatedData"
                    v-on:click="selected_item(index, item.id); showModal(item.id)"
                    :class="{'active': selected_item_index===index}">
                    <div>{{ item.name }}</div>
                    <div>
                        <button type="button" class="btn btn-outline-light but"
                                @click="deleteItem(item.id); showModal=false"
                                :variant="secondary">
                            Delete
                        </button>
                    </div>
                </li>
            </ul>
            <div v-show="pageCount>1" class='prevNext'>
                <b style="word-space:2em">&nbsp;</b>
                <button :disabled="pageNumber === 0" @click="prevPage"> Previous
                </button>
                <span v-if="pageNumber > 0 && pageNumber < pageCount-1">
                    1... <b>{{pageNumber+1 }}</b> ... {{pageCount}}
                </span>
                <span v-if="pageNumber===0">
                    <b> 1 </b> ... <b style="word-space:2em">&nbsp;</b> ... {{pageCount}}
                </span>
                <span v-if="pageNumber===pageCount-1">
                    1  ... <b style="word-space:2em">&nbsp;</b> ... <b>{{pageCount}}</b>
                </span>
                <button :disabled="pageNumber >= pageCount-1 " @click="nextPage"> Next
                </button>
                <b style="word-space:2em">&nbsp;</b>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "List_paginated",
        data() {
            return {
                size: 5,
                pageNumber: 0,
                selected_item_index: 0,
                selected_item_id: 0,
                modalShow: false

            }
        },
        props: ["title", "list", "deleteItem", "showModal"],
        methods: {
            selected_item: function (index, item) {
                this.selected_item_index = index;
                this.item_index = item;
                this.selected_item_id = item;
            },
            nextPage() {
                this.pageNumber++;
                this.selected_item_index = 0
            },
            prevPage() {
                this.pageNumber--;
                this.selected_item_index = 0
            },
        },
        computed: {
            pageCount() {
                let l = this.list.length,
                    s = this.size,
                    pageMax = (l % s != 0) ? Math.floor(l / s) + 1 : Math.floor(l / s);
                return pageMax;
            },
            paginatedData() {
                const start = this.pageNumber * this.size,
                    end = (start + this.size <= this.list.length) ? start + this.size : this.list.length;
                return this.list.slice(start, end);
            },

        },

    }
</script>

<style scoped>
    .content {
        height: 100%;
        overflow: hidden;
        margin: 0px;
        display: flex;
    }
    .paginated-list {
        width: 100%;
    }
    .column {
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .prevNext {
        display: flex;
        justify-content: space-between;
    }

    .title {
        display: flex;
        justify-content: center;
    }
    .but{
        float: right;
    }

    #left {
        flex-shrink: 0;
        background-color: whitesmoke;
        margin: 5px;
        padding: 5px;
        width: 16%;
    }

    #right {
        background-color: #f3f3f3;
        padding: 5px;
        margin: 0;
        width: 100%;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
</style>
