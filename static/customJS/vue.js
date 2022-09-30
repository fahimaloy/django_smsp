const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            notification_numbers: 0,
            notifications: [],
        };
    },
    mounted() {
        this.get_notifications();
        
    },
    methods: {
        clickedSeenAll(){
            let self = this
            $.ajax({
            url: window.location.origin+"/seen_all_notifications/",
            type: "POST",
            success: function(data){
                if(data.status == 'All Seen'){
                    self.get_notifications();
                }else{
                    console.log(data)
                }
            }
        });
        },
         clickedNotification(id,link){
            let self = this
            $.ajax({
            url: window.location.origin+"/seen_notification/"+id+"/",
            type: "POST",
            success: function(data){
                if(data.status == 'seen'){
                    self.get_notifications();
                    window.location.href = link;
                }else{
                    console.log(data)
                }
            }
        });
        },
        get_notifications() {
            let self = this;
            $.ajax({
                url: "{% url 'get_not_number' %}",
                type: "POST",
                data: {

                },
                success: function (data) {
                    self.notification_numbers = data.notnmb[0].notf
                    self.notifications = data.notifications
                },
            });
        }
    }
});
app.mount("#base_app");
