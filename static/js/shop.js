Vue.use(VueResource);


//--basket--
Vue.component('basket', {
    data: function() {
        return {
        data: '',
        }
    },
    props: ['items_in_basket', 'all_sum'],

    methods: {
        click_on_buy_all: function() {
            items_to_form = {}
            for (item of this.items_in_basket) {
                items_to_form[item.name] = item.number;
            }
            this.data = JSON.stringify(items_to_form)
        },
    },
    template: '#basket-template',
    delimiters: ['[[',']]'],
})

Vue.component('item-in-basket', {
    props: ['item'],
    computed: {
        sum_cost: function() {
            return this.item.number * this.item.cost
        }
    },
    template: '#item-in-basket-template',
    delimiters: ['[[',']]'],
})

//--shop--
Vue.component('item', {
    data: function() {
        return {
            in_basket_buttom: true,
            number: 1,
        }
    },
    props: ['item'],
    computed: {
        url: function () {
          return 'http://localhost:8080/static' + this.item.item_img
        }
    },

    methods: {
        to_parent: function(sign) {
            this.$emit('add_item_in_basket', {name: this.item.name, cost: this.item.cost, number: this.number});
        },
        click_on_buy: function() {            
            this.in_basket_buttom = false;
            this.number = 1;
            this.to_parent();
        },
        plus_one: function() {
            this.number += 1;
            this.to_parent();
        },
        minus_one: function() {
            this.number -= 1;
            if (this.number === 0) {
                this.in_basket_buttom = true;
                this.to_parent();
            } else {
                this.to_parent();
            }            
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
        items_in_basket: [],
        items_to_form: JSON.stringify(this.items_in_basket),
        login: false,
        all_sum: 0,

    },
    methods: {
        get_all_items_and_user: function() {
            this.$http.get(this.items_url).then(function(response) {
                this.items = response.data;      
            }, function() {
                console.log('no products');                 
            })

            this.$http.get(this.user_url).then(function(response) {
                this.user = response.data;
                this.login = true;            
            }, function() {
                this.login = false;   
                console.log('no user');                             
            })
        },

        add_item_in_basket_sos: function(data) {
            i = 0
            for (item of this.items_in_basket) {
                if (item.name === data.name) {
                    if (data.number === 0) {
                        this.items_in_basket.splice(i, 1);
                        this.all_sum = this.all_item_in_basket_cost();
                        return;
                    } else {
                        this.items_in_basket[i].number = data.number;
                        this.items_in_basket[i].cost_multiply_number = data.cost * data.number;
                        this.all_sum = this.all_item_in_basket_cost();
                        return;
                    }
                }
                i += 1;
            }          
            this.items_in_basket.push({name: data.name, cost: data.cost, number: data.number, cost_multiply_number: data.cost * data.number});
            this.all_sum = this.all_item_in_basket_cost();
        },  
        all_item_in_basket_cost: function() {
            sum = 0;
            for (item of this.items_in_basket) {
                sum += item.cost_multiply_number;
            }
            return sum;
        },  
    },
    created: function() {
        this.get_all_items_and_user();
    },
    delimiters: ['[[',']]']
})