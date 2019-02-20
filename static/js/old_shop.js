Vue.use(VueResource);


//--basket--
Vue.component('basket', {
    props: ['items_in_basket', 'all_sum'],
    methods: {
        click: function() {            
            console.log(this.items_in_basket);
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
            this.$emit('add_item_in_basket', {name: this.item.name, cost: this.item.cost, number: this.number}, sign);
        },
        click_on_buy: function() {            
            this.in_basket_buttom = false;
            this.number = 1;
            this.to_parent('plus');
        },
        plus_one: function() {
            this.number += 1;
            this.to_parent('plus');
        },
        minus_one: function() {
            this.number -= 1;
            if (this.number === 0) {
                this.in_basket_buttom = true;
                this.to_parent('minus');
                delete shop.items_in_basket[this.item.name];
                shop.items_in_basket.crutch = 'b'; // вью не умеет рендерить, когда я удаляю что-то по ключю, поэтому тут костыль
                shop.items_in_basket.crutch = 'a';
            } else {
                this.to_parent('minus');
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
        items_in_basket: {crutch: 'a'},
        items_to_form: {},
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
                console.log(this.user.login);
                this.items_to_form.login = this.user.login;
                this.login = true;            
            }, function() {
                console.log('no user'); 
                this.login = false;               
            })
        },

        add_item_in_basket_sos: function(data, sign) {
            Vue.set(this.items_in_basket, data.name, {cost: data.cost, number: data.number, name: data.name, sum: data.cost * data.number});
            Vue.set(this.items_to_form, data.name, data.number);

            // больше костылей богу костылей
            if (sign === 'plus') {
                this.all_sum += data.cost;
            } else {
                this.all_sum -= data.cost;
            }

            console.log(this.items_to_form);
        },          
    },
    created: function() {
        this.get_all_items_and_user();
    },
    delimiters: ['[[',']]']
})