$("#form").submit(function(e){
                e.preventDefault();
            });
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
        case 'Recommendation (Users)':
        setuprecom()
        break;
      case 'Predict Categories':
        setuppredict()
        break;
      default:
        // code block
    }
}

$('.buttons').click(()=>{
	if ($('#select-1').attr('type')=="predict"){
		predict_categories($('#select-1').val(),$('#select-2').val(),Number($('#select-3').val()),
			Number($('#select-4').val()),Number($('#select-5').val()),Number($('#select-6').val()),Number($('#select-7').val()))
	} else {
		predict_id(Number($('#select').val()))
		// predict_camera(Number($('#select-1').val()),Number($('#select-2').val()))
	}
})

function setuppredict() {
	$('.selector').html('')
   $('#form').hide()
   $('#details').hide()
	
   $('.selector').show()
   // $('#select-1').show()
   $('.predict').show()
   $('.list-group').hide()
                     $('#details').hide();

	$('#text1').html('BASED ON INTEREST IN CAMERA (USER CATEGORY)')
   $('#text2').html('BASED ON PERFORMANCE SCORE (USER CATEGORY)')
   $('#text3').html('BASED ON INTEREST IN BRANDS (USER CATEGORY)')
            
         	$('#answer1').html('')
         	$('#answer2').html('<ul></ul>')
            $('#answer3').html('<ul></ul>')
            $('#answer4').html('<ul></ul>')
	startLoader()
	$.ajax({
         url: 'http://127.0.0.1:5000/api/brand/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').append('<div class="select-container"><label for="select-1">Brand</label><select name="select-1" type ="predict" id="select-1">')
            console.log("type_of_user")
            msg.brand.forEach((t, i)=>{
            	if (i==0){
            		$('#select-1').append('<option value="" selected disabled>Select Brand</option>')
            		
            	}
            	$('#select-1').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select></div>')
            setupscore()
            
         },
         error: function(result) {
         }
           
      });
}
function setupcamera() {
	startLoader()
	$.ajax({
         url: 'http://127.0.0.1:5000/api/front_camera/all',
         method: 'GET',
         success: function(msg) {
         	$('#selector-2').append('<div class="select-container"><label for="select-6">Front Camera</label><select name="select-6" type ="front_camera" id="select-6">')
            console.log("type_of_user")
            msg.front_camera.forEach((t, i)=>{
            	if (i==0){
            		$('#select-6').append('<option value="" selected disabled>Select Front Camera (MegaPixels)</option>')
            		
            	}
            	$('#select-6').append('<option value="'+t+'">'+t+'</option>')
            })
            $('#selector-2').append('</select></div>')
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
         	$('#selector-2').append('<div class="select-container"><label for="select-7">Rear Camera</label><select name="select-7" id="select-7">')
            console.log("type_of_user")
            msg.rear_camera.forEach((t, i)=>{
            	if (i==0){
            		$('#select-7').append('<option value="" selected disabled>Select Rear Camera (MegaPixels)</option>')
            		
            	}
            	$('#select-7').append('<option value="'+t+'">'+t+'</option>')
            })
            $('#selector-2').append('</select></div>')
        
            stopLoader()
         },
         error: function(result) {
         }
           
      });
}
function setupscore() {
	$.ajax({
         url: 'http://127.0.0.1:5000/api/processor/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').append('<div class="select-container"><label for="select-2">Processor</label><select name="select-2" type ="processor" id="select-2">')
            console.log("type_of_user")
            msg.processor.forEach((t, i)=>{
            	if (i==0){
            		$('#select-2').append('<option value="" selected disabled>Select Processor</option>')
            		
            	}
            	$('#select-2').append('<option value="'+t+'">'+t+'</option>')
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
         	$('.selector').append('<div class="select-container"><label for="select-3">RAM</label><select name="select-3" type ="processor" id="select-3">')
            console.log("type_of_user")
            msg.ram.forEach((t, i)=>{
            	if (i==0){
            		$('#select-3').append('<option value="" selected disabled>Select RAM (GigaBytes)</option>')
            		
            	}
            	$('#select-3').append('<option value="'+t+'">'+t+'</option>')
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
         	$('.selector').append('<div class="select-container"><label for="select-4">Storage</label><select name="select-4" type ="processor" id="select-4">')
            console.log("type_of_user")
            msg.storage.forEach((t, i)=>{
            	if (i==0){
            		$('#select-4').append('<option value="" selected disabled>Select Storage (GigaBytes)</option>')
            		
            	}
            	$('#select-4').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select></div>')
            setupbattery()
           
         },
         error: function(result) {
         }
           
      });
}

function setupbattery() {
	$('#selector-2').html('')
	$.ajax({
         url: 'http://127.0.0.1:5000/api/battery/all',
         method: 'GET',
         success: function(msg) {
         	$('#selector-2').append('<div class="select-container"><label for="select-5">Battery</label><select name="select-5" type ="processor" id="select-5">')
            console.log("type_of_user")
            msg.battery.forEach((t, i)=>{
            	if (i==0){
            		$('#select-5').append('<option value="" selected disabled>Select Battery (MAAh)</option>')
            		
            	}
            	$('#select-5').append('<option value="'+t+'">'+t+'</option>')
            })
            $('#selector-2').append('</select></div>')
            setupcamera()
            
         },
         error: function(result) {
         }
           
      });
}
setuppredict()
function setuprecom() {
	$('#text1').html('Recommend on basis of his interest in BRANDS')
         	$('#text2').html('Recommend on basis of his interest in phone')
         	$('#text3').html('Recommend on basis of his interest in camera')
         	$('#answer1').html('')
         	$('#answer2').html('<ul></ul>')
         	$('#answer3').html('<ul></ul>')
	$('.selector').hide()
   // $('#select-1').hide()
   $('.predict').hide()
   $('#answer-container').css('visibility', 'hidden');
   $('#form').show()
$('#details').hide();
   $('.list-group').hide()
                     // $('#details').hide();

	$('.selector').html('')
	startLoader()
	$.ajax({
         url: 'http://127.0.0.1:5000/api/id/all',
         method: 'GET',
         success: function(msg) {
         	$('.selector').append('<select name="select-1" id="select">')
            console.log("type_of_user")
            msg.id.forEach((t, i)=>{
            	if (i==0){
            		$('#select').append('<option value="" selected disabled>Select User ID</option>')
            		
            	}
            	$('#select').append('<option value="'+t+'">'+t+'</option>')
            })
            $('.selector').append('</select>')
            stopLoader()
            
         },
         error: function(result) {
         }
           
      });

}

function predict_categories(brand, processor, ram, storage, battery, front_camera, rear_camera) {
	startLoader()
	console.log(brand)
	$.ajax({
         url: 'http://127.0.0.1:5000/api/predict/mobile/categories',
         method: 'POST',
         processData: false,
        contentType: 'application/json',
         data: JSON.stringify({
         	brand:brand,
         	processor:processor,
         	ram:ram,
         	storage:storage,
         	battery:battery,
            front_camera:front_camera,
            rear_camera:rear_camera   
         }),

         success: function(msg) {
         	console.log(msg)
         	$('#text1').html(msg['categories'][1].desp)
         	$('#text2').html(msg['categories'][0].desp)
         	$('#text3').html(msg['categories'][2].desp)
         	$('#answer1').html(msg['categories'][1].name)
         	$('#answer2').html(msg['categories'][0].name)
         	if (brand == "Apple" || brand == "Samsung" || brand == "LG"){
         		$('#answer3').html('<strong>'+brand+' Lovers</strong>')
         	} else {
         		$('#answer3').html('<strong>Brand Lovers aren\'t Interested<strong>')
         	}
            stopLoader()
            
         },
         error: function(result) {
         }
           
      });

}
function predict_id(id) {
	startLoader()
   console.log(id)
	// console.log(brand)
	$.ajax({
         url: 'http://127.0.0.1:5000/api/predict/id/recommend',
         method: 'POST',
         processData: false,
        contentType: 'application/json',
         data: JSON.stringify({
         	id:id,
         	   
         }),

         success: function(msg) {
   $('#answer-container').css('visibility', 'visible');

         	console.log(msg)
   $('#details').show()

         	$('#text1').html(msg['categories'][0].desp)
         	$('#text2').html(msg['categories'][1].desp)
         	$('#text3').html(msg['categories'][2].desp)
         	$('#answer1').html(msg['categories'][0].name)
         	$("#answer2").html('<ul id="a"></ul>')
         	msg['categories'][1].name.forEach((t)=>{
         		$("#a").append('<li>'+t+'</li>')
            })
            $('#answer4').html(msg['categories'][3])
         	
         		
         	if(typeof(msg['categories'][2].name)=="string") {
         		$('#answer3').html(msg['categories'][2].name)
         	} else {
         		$("#answer3").html('<ul id="b"></ul>')
         	msg['categories'][2].name.forEach((t)=>{
         		$("#b").append('<li>'+t+'</li>')
         	})
         	}
            stopLoader()
            
         },
         error: function(result) {
         }
           
      });
}
$("#searchbar").click(function(event){
   $('#details').hide();
   $('#answer-container').css('visibility', 'hidden');

});
$("#searchbar").keyup(function(event){
   $('#details').hide();
   $('#answer-container').css('visibility', 'hidden');
   var character = $("#searchbar").val()
   searchData(character);
});

function getData(e){
console.log(e.getAttribute('ID'))
   predict_id(Number(e.getAttribute('ID')))
   predict_details(Number(e.getAttribute('ID')),e.innerHTML)
   $('.list-group').hide()
                     // $('#details').hide();

   $("#searchbar").val(e.innerHTML)
}
function predict_details(id,name) {
   $.ajax({
         url: 'http://127.0.0.1:5000/api/get_category_of_user',
         method: 'POST',
         processData: false,
        contentType: 'application/json',
         data: JSON.stringify({
            id:id,
           

         }),

         success: function(msg) {
   // $('#answer-container').css('visibility', 'visible');
            console.log('god')
            console.log(msg)
             $('#id').html('ID : '+msg['ID'])
            
            $('#name').html('Name : '+name.charAt(0).toUpperCase() + name.slice(1))
            $('#Total_Purchases').html('Total Purchases : '+msg['Total_Purchased'])

            
         },
         error: function(result) {
         }
           
      });
}

function searchData(character) {
   $.ajax({
      url:'http://127.0.0.1:5000/api/get/name',
      method: 'POST',
        processData: false,
        contentType: 'application/json',
         data: JSON.stringify({
            char:character,
               
         }),
                  success: function (msg) {
                  $('.list-group').html('');
                  if (msg['data'].length > 0 && character.length>0) {
                     $('.list-group').show();
                     // $('.details').show();

                     msg['data'].forEach((user)=>{
                        $('.list-group').append('<li onclick="getData(this);" class="list-group-item" ID="'+user.ID+'">'+user.name+'</li>')
                     })
                  } else {
                     $('.list-group').hide();
                     // $('#details').hide();

                  }
                  
                     
                  },
                    error: function (result) {
                        console.log("Error Occured");
                    }
   });
}