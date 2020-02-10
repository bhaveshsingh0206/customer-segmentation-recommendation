function startLoader() {
    document.querySelector('.loader').classList.remove('hidden');
}

function stopLoader() {
    document.querySelector('.loader').classList.add('hidden');
}

google.charts.load('current', { packages: ['bar'] });
google.charts.load('current', { packages: ['corechart'] });

function drawBarChart(msg) {
    startLoader()
    var temp = [[msg.x_axis,msg.y_axis]]
    msg.categories.forEach((dat)=>{
        var t = []
        t.push(dat.name)
        t.push(dat.value)
        temp.push(t)
    })
    var data = new google.visualization.arrayToDataTable(
        temp
    );

    var options = {
        title: msg.description,
        colors: ['#1e88e5'],
        width: 800,
        height: 500
    };

    // var chart = new google.charts.Bar(document.getElementById('top_x_div'));

    var chart = new google.charts.Bar(document.getElementById('chart'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
    stopLoader()
}

function drawPieChart(msg) {
    startLoader()
    var temp = [[msg.x_axis,msg.y_axis]]
    msg.categories.forEach((dat)=>{
        var t = []
        // console.log(typeof(dat.name))
        t.push(dat.name.toString())
        t.push(dat.value)
        temp.push(t)
    })
    var data = new google.visualization.arrayToDataTable(
        temp
    );

    var options = {
        title: msg.description,
        pieHole: 0.3,
        width: 800,
        height: 550,
        is3D: true
    };

    var chart = new google.visualization.PieChart(
        document.getElementById('chart')
    );
    chart.draw(data, options);
    stopLoader()
}


function switchVal(data) {
    switch(data.value) {
case 'item_count':
    get_setupitem()
    break;
    case 'pay':
    get_pay()
    break;
  case 'category':
    get_category_of_user()
    break;
  case 'frequency':
    type_of_user()
    break;
case 'memory':
    get_memory()
    break;
case 'storage':
    get_storage()
    break;
case 'front_camera':
    get_front()
    break;
    case 'rear_camera':
    get_rear()
    break;

  default:
    get_country_details(data.value)

    }
}
    function get_country_details(dat) {
        console.log(dat)
        startLoader()
        $.ajax({
         url: 'http://127.0.0.1:5000/api/country/details',
         method: 'POST',
         processData: false,
        contentType: 'application/json',
         data: JSON.stringify({
            country:dat
         }),
         success: function(msg) {
            console.log("get_country_details")
            google.charts.setOnLoadCallback(()=>{drawPieChart(msg)})
            stopLoader()
         },
         error: function(result) {
         }
           
      });
    }
    function select(selectedElement) {
        document.querySelectorAll('.sidebar a').forEach(element => {
            element.classList.remove('selected');
        });
        selectedElement.classList.add('selected');
        console.log(selectedElement.textContent)
        switch(selectedElement.textContent) {
        case 'Buying Behaviour':
        setupDemo()
        break;
      case 'Geography':
        setupgeog()
        break;
        case 'Purchases':
        setupitem()
    break;
        case 'Features':
        setupfea()
        get_memory()
        break;
        case 'Payment Type':
        setuppay()
        break;
      default:
        // code block
    }
}

    function setupgeog() {
        startLoader()
        $('#title').html('Analytics based on Geography')
        $('#select-menu').html('')
        $('#select-menu').show()
        $.ajax({
         url: 'http://127.0.0.1:5000/api/country/all',
         method: 'GET',
         success: function(msg) {
            // console.log(msg)
            $('#select-menu').html('')
            msg.countries.forEach((t, i)=>{
                // console.log(t)
                $('#select-menu').append('<option value="'+t+'">'+t+'</option>')
                if(i==0) {
                    get_country_details(t)
                }
            })
            stopLoader()
         },
         error: function(result) {
         }
           
      });
    }
    function setupitem() {
        // $('#select-menu').hide()
        get_setupitem()
    }
    function setupfea() {
        $('#title').html('Analytics based on Features ( Memory, Storage, Camera )')

        $('#select-menu').html('')
        $('#select-menu').show()
        $('#select-menu').append('<option value="memory">Memory</option><option value="storage">Storage</option><option value="rear_camera">Rear camera</option><option value="front_camera">Front camera</option>')
    }
    function setuppay() {
        // $('#select-menu').hide()
        get_pay()
    }


function get_setupitem() {
    startLoader()
    $.ajax({
         url: 'http://127.0.0.1:5000/api/purchase/counts',
         method: 'GET',
         success: function(msg) {
            console.log("purchase/counts")
            google.charts.setOnLoadCallback(()=>{drawBarChart(msg)})
            stopLoader()
         },
         error: function(result) {
         }
           
      }); 
}
function get_pay() {
    startLoader()
    $.ajax({
         url: 'http://127.0.0.1:5000/api/payment/details',
         method: 'GET',
         success: function(msg) {
            console.log("get_category_of_user")
            google.charts.setOnLoadCallback(()=>{drawBarChart(msg)})
            stopLoader()
         },
         error: function(result) {
         }
           
      }); 
}
get_category_of_user()
function get_category_of_user() {
    // startLoader()
   $.ajax({
         url: 'http://127.0.0.1:5000/api/get_category_of_user',
         method: 'GET',
         success: function(msg) {
            console.log("get_category_of_user")
            google.charts.setOnLoadCallback(()=>{drawBarChart(msg)})
            stopLoader()
         },
         error: function(result) {
         }
           
      }); 
}
function get_memory() {
    startLoader()
   $.ajax({
         url: 'http://127.0.0.1:5000/api/ram/counts',
         method: 'GET',
         success: function(msg) {
            console.log("ram/counts")
            google.charts.setOnLoadCallback(()=>{drawPieChart(msg)})
            stopLoader()
         },
         error: function(result) {
         }
           
      }); 
}
function get_storage() {
    startLoader()
   $.ajax({
         url: 'http://127.0.0.1:5000/api/storage/counts',
         method: 'GET',
         success: function(msg) {
            console.log("storage/counts")
            google.charts.setOnLoadCallback(()=>{drawPieChart(msg)})
            stopLoader()
         },
         error: function(result) {
         }
           
      }); 
}
function get_front() {
    startLoader()
   $.ajax({
         url: 'http://127.0.0.1:5000/api/front_camera/counts',
         method: 'GET',
         success: function(msg) {
            console.log("front_camera/counts")
            google.charts.setOnLoadCallback(()=>{drawPieChart(msg)})
            stopLoader()
         },
         error: function(result) {
         }
           
      }); 
}
function get_rear() {
    startLoader()
   $.ajax({
         url: 'http://127.0.0.1:5000/api/rear_camera/counts',
         method: 'GET',
         success: function(msg) {
            console.log("rear_camera/counts")
            google.charts.setOnLoadCallback(()=>{drawPieChart(msg)})
            stopLoader()
         },
         error: function(result) {
         }
           
      }); 
}
function setupDemo() {
    console.log("called")
        $('#title').html('Analytics based on Buying Behaviour')

        $('#select-menu').html('')
        $('#select-menu').show()
        $('#select-menu').append('<option value="category">Category</option><option value="frequency">Frequency</option><option value="item_count">Items Count</option><option value="pay">Payment</option>')
        get_category_of_user()

        
    }

function type_of_user() {
    startLoader()
    $.ajax({
         url: 'http://127.0.0.1:5000/api/type_of_user',
         method: 'GET',
         success: function(msg) {
            console.log("type_of_user")
            google.charts.setOnLoadCallback(()=>{drawBarChart(msg)})
            stopLoader()
         },
         error: function(result) {
         }
           
      });
}


