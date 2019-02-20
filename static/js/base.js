var base = new Vue ({
    el: '#base',
    data: {
        mobile_mod: false,
        show_aside: false,
    },
    methods: {
        switch_on_mobile_mod: function() {
            if (window.innerWidth >= 777) {
                this.mobile_mod = false;
                this.show_aside = false;
            } else if (window.innerWidth < 777) {
                this.mobile_mod = true;
            }
        },
    },
    created: function() {
        this.switch_on_mobile_mod();
    },
    delimiters: ['[[',']]']
})