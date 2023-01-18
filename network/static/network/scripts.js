document.addEventListener("DOMContentLoaded", () => {


    // Set dynamic page height
    if (!document.querySelector('.alert')) {
        document.querySelector('.content').style.height = `calc(100vh - ${document.querySelector('.navbar').offsetHeight}px)`;
    } else {
        document.querySelector('.content').style.height = `calc(100vh - ${document.querySelector('.navbar').offsetHeight}px - ${document.querySelector('.alert').offsetHeight}px)`;
    }

    // On click, show the div for user to create a new post
    document.querySelector('#create-post-button').addEventListener('click', () => {
        document.querySelector('#new-post').style.display = 'block';
        document.querySelector('#create-post-button').style.display = 'none';
    });
   
    // On click, hide the div for user to create a new post
    document.querySelector('#close-new-post').addEventListener('click', () => {
        document.querySelector('#id_post').value = '';
        document.querySelector('#new-post').style.display = 'none';
        document.querySelector('#create-post-button').style.display = 'block';
    });

    // On click, make the post editable if the post belongs to the user
    document.querySelectorAll('.edit').forEach((element) => {
        element.onclick = function() {
            // Hide edit button
            element.style.display = "none";
            // Show save button
            element.nextElementSibling.style.display = "inline";
            // Get current post text div
            const postDivText = element.parentElement.parentElement.parentElement.querySelector('.card-text');
            // Replace p with textarea
            const editText = document.createElement('textarea')
            editText.classList.add("form-control")
            editText.classList.add('card-text')
            editText.innerHTML = postDivText.innerHTML.trim()
            postDivText.replaceWith(editText)
            // // Set cursour to end of string
            const end = editText.innerHTML.length;
            editText.setSelectionRange(end, end)
            editText.focus();
        };
    });

    // On click, make the post uneditable and save the changes to database
    document.querySelectorAll('.save-changes').forEach((element) => {
        element.onclick = function() {
            // Hide save button
            element.style.display = "none";
            // Show edit button
            element.previousElementSibling.style.display = "inline";
            // Get updated text
            const postDivText = element.parentElement.parentElement.parentElement.querySelector('.card-text');
            // Replace p with textarea
            const editedText = document.createElement('p')
            editedText.classList.add('card-text')
            editedText.innerHTML = postDivText.value.trim()
            postDivText.replaceWith(editedText)
            // Send updated text to database
            const postId = element.parentElement.parentElement.parentElement.getAttribute('id').slice(5);
            const csrftoken = element.previousElementSibling.previousElementSibling.value;
            fetch(`/posts/${postId}`, {
                method: 'PUT',
                headers:{
                    'X-csrftoken': csrftoken
                },
                body: JSON.stringify({
                    post: editedText.textContent,
                })
            });
        };
    });

    // On click, delete the post if the post belongs to the user
    document.querySelectorAll('.delete').forEach((element) => {
        element.onclick = function() {
            element.parentElement.parentElement.parentElement.style.display = 'none';
            const csrftoken = element.previousElementSibling.previousElementSibling.previousElementSibling.value;
            const postId = element.parentElement.parentElement.parentElement.getAttribute('id').slice(5);
            fetch(`/delete_post/${postId}`, {
                method: 'DELETE',
                headers:{
                    'X-csrftoken': csrftoken
                }
            });
        };
    });

    // like button
    document.querySelectorAll('.like-button').forEach((element) => {
        element.onclick = function() {
            let likes = parseInt(element.innerHTML);
            const postId = element.parentElement.parentElement.parentElement.getAttribute('id').slice(5);
            const csrftoken = element.previousElementSibling.value;
            fetch(`/like_post/${postId}`, {
                method: 'POST',
                headers:{
                    'X-csrftoken': csrftoken
                },
                body: JSON.stringify({
                    post: postId
                })
            })
            .then(response => response.json())
            .then(result => {
                if (result.message === 'Like added') {
                    likes++;
                    element.innerHTML = likes;
                } else if (result.message === 'Like removed') {
                    likes--;
                    element.innerHTML = likes;
                }
            });
        };
    });
})

