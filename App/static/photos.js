        // Define a function
        function upload() {
            window.location.href = "/upload";
        }
        function logout() {
            window.location.href = "/logout";
        }
        function home() {
        window.location.href = "/";
        }
                function showConfirmation() {
            var modal = document.getElementById("confirmationModal");
            modal.style.display = "block";
        }

        function confirmDelete() {
            var form = document.querySelector("form");
            form.submit();
        }

        function cancelDelete() {
            var modal = document.getElementById("confirmationModal");
            modal.style.display = "none";
        }