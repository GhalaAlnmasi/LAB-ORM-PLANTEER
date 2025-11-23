document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu
  const mobileBtn = document.getElementById("mobileMenuBtn");
  const mobileMenu = document.getElementById("mobileMenu");

  if (mobileBtn) {
    mobileBtn.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
    });
  }

  // Filters toggle
  window.toggleFilters = function () {
    const filterForm = document.getElementById("filter-form");
    const filterIcon = document.getElementById("filter-icon");
    const filterIconOff = document.getElementById("filter-icon-off");

    filterForm.classList.toggle("hidden");
    filterIcon.classList.toggle("hidden");
    filterIconOff.classList.toggle("hidden");
  };

  // Clear filters
  window.clearFilters = function () {
    const url = new URL(window.location.href);
    url.searchParams.delete("category");
    url.searchParams.delete("is_edible");
    window.location.href = url.toString();
  };

  // Comment form toggle
  const commentBtn = document.getElementById("toggleCommentForm");
  const commentForm = document.getElementById("commentFormContainer");

  if (commentBtn) {
    commentBtn.addEventListener("click", () => {
      commentForm.classList.toggle("hidden");
    });
  }
});
