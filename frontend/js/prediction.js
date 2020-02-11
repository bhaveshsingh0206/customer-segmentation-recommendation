function startLoader() {
    document.querySelector('.loader').classList.remove('hidden');
}

function stopLoader() {
    document.querySelector('.loader').classList.add('hidden');
}


function select(selectedElement) {
        document.querySelectorAll('.sidebar a').forEach(element => {
            element.classList.remove('selected');
        });
        selectedElement.classList.add('selected');
        console.log(selectedElement.textContent)
        switch(selectedElement.textContent) {
        case 'Predict Brand':
        // $('select-2').attr('disabled', 'disabled');

        setupbrand()
        break;
      case 'Predict Performance Score':
        setupscore()
        break;
    break;
        case 'Predict User Category':
        setupcamera()
        break;
      default:
        // code block
    }
}
function setupcamera() {
    $('#title').html('Predict User Category based on Camera Specs')
    
	$('#text').html('Above Specification suits')
	$('#answer').html('')
	$('.selector').html('')
	startLoader()
	$.ajax({
         url: 'http://127.0.0.1:5000/api/front_camera/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').append('<div class="select-container"><label for="select-1">Front Camera (in MP)</label><select name="select-1" type ="front_camera" id="select-1">')
            console.log("type_of_user")
            msg.front_camera.forEach((t, i)=>{
            	if (i==0){
            		$('#select-1').append('<option value="" selected disabled>Select Front Camera</option>')
            		
            	}
            	$('#select-1').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select></div>')
            setupback()
            
         },
         error: function(result) {
         }
           
      });
}
function setupback() {
	$.ajax({
         url: 'http://127.0.0.1:5000/api/rear_camera/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').append('<div class="select-container"><label for="select-2">Rear Camera (in MP)</label><select name="select-2" id="select-2">')
            console.log("type_of_user")
            msg.rear_camera.forEach((t, i)=>{
            	if (i==0){
            		$('#select-2').append('<option value="" selected disabled>Select Rear Camera</option>')
            		
            	}
            	$('#select-2').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select></div>')
        
            stopLoader()
         },
         error: function(result) {
         }
           
      });
}
function setupscore() {
    $('#title').html('Predict Performance Score based on Technical Specifications')
	$('#text').html('Predicted score of the above SPECIFICATION mobile is')
	$('#answer').html('')
	$('.selector').html('')
	startLoader()
	$.ajax({
         url: 'http://127.0.0.1:5000/api/processor/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').append('<div class="select-container"><label for="select-1">Processor</label><select name="select-1" type ="processor" id="select-1">')
            console.log("type_of_user")
            msg.processor.forEach((t, i)=>{
            	if (i==0){
            		$('#select-1').append('<option value="" selected disabled>Select Processor</option>')
            		
            	}
            	$('#select-1').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select></div>')
            setupmemory()
            
         },
         error: function(result) {
         }
           
      });
}
function setupmemory() {
	
	$.ajax({
         url: 'http://127.0.0.1:5000/api/ram/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').append('<div class="select-container"><label for="select-2">RAM (in GB)</label><select name="select-2" type ="processor" id="select-2">')
            console.log("type_of_user")
            msg.ram.forEach((t, i)=>{
            	if (i==0){
            		$('#select-2').append('<option value="" selected disabled>Select RAM</option>')
            		
            	}
            	$('#select-2').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select></div>')
            setupstorage()
            
         },
         error: function(result) {
         }
           
      });
}
function setupstorage() {
	
	$.ajax({
         url: 'http://127.0.0.1:5000/api/storage/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').append('<div class="select-container"><label for="select-3">Storage (in GB)</label><select name="select-3" type ="processor" id="select-3">')
            console.log("type_of_user")
            msg.storage.forEach((t, i)=>{
            	if (i==0){
            		$('#select-3').append('<option value="" selected disabled>Select Storage (GigaBytes)</option>')
            		
            	}
            	$('#select-3').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select></div>')
            setupbattery()
           
         },
         error: function(result) {
         }
           
      });
}

function setupbattery() {
	
	$.ajax({
         url: 'http://127.0.0.1:5000/api/battery/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').append('<div class="select-container"><label for="select-4">Battery (in mAh)</label><select name="select-4" type ="processor" id="select-4">')
            console.log("type_of_user")
            msg.battery.forEach((t, i)=>{
            	if (i==0){
            		$('#select-4').append('<option value="" selected disabled>Select Battery</option>')
            		
            	}
            	$('#select-4').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select></div>')
            
            stopLoader()
         },
         error: function(result) {
         }
           
      });
}


setupbrand()
function setupbrand() {
    $('#title').html('Predict Brand based of City and State')


	$('#text').html('MOST POPULAR PHONES IN THIS PARTICULAR CITY')
	$('#answer').html('')
	console.log('setupbrand')
	// $('.selector').html('<select name="select-1" onchange="setupstates(this.value);" type ="city" id="select-1"><select name="select-2" id="select-2"></select>')
	startLoader()
    $.ajax({
         url: 'http://127.0.0.1:5000/api/states/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').html('<div class="select-container"><label for="select-1">State</label><select name="select-1" onchange="setupcities(this.value);" type ="city" id="select-1"></select></div><div class="select-container"><label for="select-2">City</label><select name="select-2" id="select-2"></select></div>')
            console.log("type_of_user")
            msg.states.forEach((t, i)=>{
            	if (i==0){
            		$('#select-1').append('<option value="" selected disabled>Select State</option>')
            		$('#select-2').append('<option value="" selected disabled>Select City</option>')
            	}
            	$('#select-1').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select>')
            
            stopLoader()
         },
         error: function(result) {
         }
           
      });
}

function setupstates(city) {
    $('#select-2').html('<option value="" selected disabled hidden>Select State</option>')
	startLoader()
    // $('select-2').removeAttr('disabled');
    console.log(city)
    $.ajax({
         url: 'http://127.0.0.1:5000/api/states',
         method: 'POST',
         processData: false,
        contentType: 'application/json',
         data: JSON.stringify({
            city:city   
         }),
         
         success: function(msg) {
            // $('select-2').removeAttr('disabled');
            // $('.selector').html('')
            // $('.selector').html('<select name="select-1" onchange="setupstates(this.value);" type ="city" id="select-1">')

         	// $('.selector').append('<select name="select-2" id="select-2">')
            // $('#select-2').html('')
            console.log("type_of_user")
            msg.states.forEach((t, i)=>{
            	if (i==0){
            		$('#select-2').append('<option value="" selected disabled>Select State</option>')
            		
            	}
            	$('#select-2').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select>')
            stopLoader()
         },
         error: function(result) {
         }
           
      });
}

function setupcities(state) {
   $('#select-2').html('<option value="" selected disabled hidden>Select City</option>')
  startLoader()
   // $('select-2').removeAttr('disabled');
   console.log(state)
   $.ajax({
        url: 'http://127.0.0.1:5000/api/cities',
        method: 'POST',
        processData: false,
       contentType: 'application/json',
        data: JSON.stringify({
           state:state   
        }),
        
        success: function(msg) {
           // $('select-2').removeAttr('disabled');
           // $('.selector').html('')
           // $('.selector').html('<select name="select-1" onchange="setupstates(this.value);" type ="city" id="select-1">')

           // $('.selector').append('<select name="select-2" id="select-2">')
           // $('#select-2').html('')
           console.log("type_of_user")
           msg.cities.forEach((t, i)=>{
              if (i==0){
                 $('#select-2').append('<option value="" selected disabled>Select City</option>')
                 
              }
              $('#select-2').append('<option value="'+t+'">'+t+'</option>')
           })
           $('.selector').append('</select>')
           stopLoader()
        },
        error: function(result) {
        }
          
     });
}
function switchVal(data) {
    switch(data.value) {
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

$('.buttons').click(()=>{
	// predict_score($('#select-1').val(),$('#select-2').val(),$('#select-3').val(),$('#select-4').val())
	if ($('#select-1').attr('type')=='city'){
		predict_brand($('#select-1').val(),$('#select-2').val())
	} else if($('#select-1').attr('type')=='processor'){
		predict_score($('#select-1').val(),$('#select-2').val(),$('#select-3').val(),$('#select-4').val())
	} else {
		predict_camera(Number($('#select-1').val()),Number($('#select-2').val()))
	}
})




function predict_brand(city, state) {
    console.log(city,state)
    startLoader()
        $.ajax({
         url: 'http://127.0.0.1:5000/api/predict/brand',
         method: 'POST',
         processData: false,
        contentType: 'application/json',
         data: JSON.stringify({
            city:state,
            state:city
         }),
         success: function(msg) {
            // console.log(msg)
            $('#text').html('MOST POPULAR PHONES IN THIS PARTICULAR CITY')
            // console.log(msg.replace(/\'/g,'').split(' '))
            $('#answer').html('<ul id="a"><ul>')
            $('#a').html('')
            var tem = msg.replace(/\'/g,'').split(' ')
            tem.forEach((t)=>{
                console.log(t)
                if (t != ""){                                               
                    $('#a').append('<li>'+t+'</li>')
                }
                
            })

            stopLoader()
         },
         error: function(result) {
         }
           
      });
    }
function predict_score(processor, ram, storage, battery) {
    startLoader()
        $.ajax({
         url: 'http://127.0.0.1:5000/api/predict/score',
         method: 'POST',
         processData: false,
        contentType: 'application/json',
         data: JSON.stringify({
            processor:processor,
            ram:ram,
            storage:storage,
            battery:battery    
         }),
         success: function(msg) {
            console.log(msg)
            $('#text').html('Predicted score of the above mobile SPECIFICATION is')
            $('#answer').html(msg['score']+' - '+msg['category'])

            stopLoader()
         },
         error: function(result) {
         }
           
      });
}

function predict_camera(front_camera, rear_camera) {
    startLoader()
        $.ajax({
         url: 'http://127.0.0.1:5000/api/predict/camera',
         method: 'POST',
         processData: false,
        contentType: 'application/json',
         data: JSON.stringify({
            front_camera:front_camera,
            rear_camera:rear_camera,   
         }),
         success: function(msg) {
            console.log(msg)
            $('#text').html('Above Specification suits')
            $('#answer').html(msg)


            stopLoader()
         },
         error: function(result) {
         }
           
      });


}



