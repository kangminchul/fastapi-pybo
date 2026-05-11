<script>
    import  {push} from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let subject = ""
    let content = ""

    function post_question(event){
        event.preventDefault()
        let url = "/api/question/create"
        let params = {
            subject : subject,
            content : content,
        }
        fastapi('post',url,params, 
            (json)=>{
                push("/")
            },
            (json_error) => {
                error = json_error
            }            
        )
    }
</script>

<Error error={error} /> 


<div class="container ">
    <!-- 질문 -->
    <h5 class="my-3 border-bottom pb-2">질문등록</h5>
    <form method="post" class="my-3">
        <div class="mb-3">
            <lable for="subject">제목</lable>        
            <input type="text" class="form-control"  bind:value="{subject}" />
        </div>
        <div class="mb-3">
            <lable for="content">내용</lable>        

            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{post_question}">저장하기</button>
    </form>
</div>
