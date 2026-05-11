<script>
    import  {push} from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

 //   alert('1')
 
    export let params = {}
    const answer_id = params.answer_id

    let error = {detail:[]}
    let question_id = ""
    let content = ""

    fastapi('get', "/api/answer/detail/" + answer_id, {}, 
                (json)=>{
                    question_id = json.question_id
                    content = json.content
                }
            )    
    alert('answer_id' + answer_id)

    function update_answer(event){
        event.preventDefault()
        let url = "/api/answer/update"
        let params = {
            answer_id : answer_id,
            content : content,
        }

        fastapi('put',url,params, 
            (json)=>{
                push("/detail/"+question_id)
            },
            (json_error) => {
                error = json_error
            }            
        )
    }
</script>



<div class="container ">
    <h5 class="my-3 border-bottom pb-2">답변 수정</h5>
    <Error error={error} /> 
    <form method="post" class="my-3">
        <div class="mb-3">
            <lable for="content">내용</lable>        
            <input type="text" class="form-control"  bind:value="{content}" />
        </div>
        <button class="btn btn-primary" on:click="{update_answer}">수정하기</button>
    </form>
</div>
