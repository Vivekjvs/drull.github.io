const comment = document.querySelector('#comment')
const add_comment = document.querySelector('#add-comment')
const list = document.querySelectorAll('.delete')
device_id = comment.dataset.device_id

for(let i=0;i<list.length;i++){
  list[i].addEventListener('click',function(e){
      $.ajax({
        method:'DELETE',
        url:'/api/comment?comment_id='+encodeURIComponent(this.dataset.comment_id),
      }).done(function(res){
        if(res.status == 'ok'){
          location.reload()
        }else{
          console.log(res)
        }
      })
    })
}
comment.addEventListener('keypress',function(e){
  if(e.which == 13 && comment.value.length <= 100){
    console.log(device_id)
    $.ajax({
      method:'POST',
      url : '/api/comment',
      data : {text:comment.value,device_id:device_id}
    }).done((obj)=>{
      if(obj.course){
        location.href = obj.course
      }else{
        comment.value = ""
        location.reload()
      }
    })
  }
})
add_comment.addEventListener('click',function(e){
  if(comment.value.length > 0 && comment.value.length <= 100){
    console.log(device_id)
    $.ajax({
      method:'POST',
      url : '/api/comment',
      data : {text:comment.value,device_id:device_id}
    }).done((obj)=>{
      if(obj.course){
        location.href = obj.course
      }else{
        comment.value = ""
        location.reload()
      }
    })
  }
})
