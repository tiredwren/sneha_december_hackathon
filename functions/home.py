import streamlit as st

def fun():
    # header
    st.title("Home:sun_with_face:")
    st.write("""Hello there! This is an application that can help people identify and describe emotions.
                This kind of emotion recognition doesn't come as easily to some people as it does to others
                , and that's perfectly okay!"""
                )
    st.write(
        "People with alexithymia have trouble recognizing the emotions of others, as well as their own emotions. " +
        "Many people with autism tend to have alexithymia, but it occurs in many others as well. Often, they are " +
        "unable to verbalize their own emotions, due to either an unawareness of, or a confusion of, emotional and bodily feelings. " +
        "Some main characteristics of alexithymia include *difficulty identifying feelings and distinguishing* " +
        "*between bodily and emotional sensations, difficulty describing feelings to others, and reduced capicity to imagine.* " + 
        "Lack of awareness of the emotions of themselves and other people around them can lead to social issues."
    )
    st.write(
        "This website is mainly geared towards helping people with alexithymia identify and describe their emotions. " +
        "Feel free to explore this website, which includes the following: "
    )
    st.write(
        ":notebook: a :orange[diary] to log the events that happen in your life, and to explore the way you may be feeling about them."
    )
    st.write(
        ":camera: a :green[camera] to detect the emotions of others around you, and perhaps also yourself! Test it out!"
    )
    st.write(
        ":pencil: a :blue[text box] to paste text into. Our app can provide insight into what emotions the text may be carrying."
    )
    st.write(
        ":question: an :violet[additional help] page to explore more resources for alexithymia!"
    )

if __name__ == "__main__":
    fun()