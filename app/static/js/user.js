$(".follow-button").on("click", toggleFollow);

async function toggleFollow(e) {
    const FollowButton = $(e.target);
    const userId = FollowButton.data("id");

    const res = await axios({
        url: `/users/toggle_follow/${userId}`,
        method: "POST",
    });

    if (res.status === 200) {
        if (FollowButton.text().includes("Follow")) {
            FollowButton.text("Unfollow");
        } else if (FollowButton.text().includes("Unfollow")) {
            FollowButton.text("Follow");
        }

        const followers = res.data["followers"];
        const following = res.data["following"];

        $(".followers-count .count").text(followers);
        $(".followers").text(followers);
        $(".following").text(following);
    }
}
