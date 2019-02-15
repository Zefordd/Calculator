Vue.use(VueResource);

Vue.component('item', {
    data: function() {
        return {
            item_data: [],
        }
    },
    props: ['item'],
    computed: {
        url: function () {
          return 'http://localhost:8080/static' + this.item.item_img
        }
    },
    template: '#item-template',
    delimiters: ['[[',']]'],
})




var shop = new Vue ({
    el: '#shop',
    data: {
        items_url: 'http://localhost:8080/shop/items_info',
        user_url: 'http://localhost:8080/shop/customer_info',
        items: [],
        user: [],
        login: false,
    },
    methods: {
        get_all_items_and_user: function() {
            this.$http.get(this.items_url).then(function(response) {
                console.log(response);
                this.items = response.data;      
            }, function() {
                console.log('no products');                 
            })
            this.$http.get(this.user_url).then(function(response) {
                this.user = response.data;
                this.login = true;            
            }, function() {
                console.log('no user'); 
                this.login = false;               
            })
        }
    },
    created: function() {
        this.get_all_items_and_user();
    },
    delimiters: ['[[',']]']
})