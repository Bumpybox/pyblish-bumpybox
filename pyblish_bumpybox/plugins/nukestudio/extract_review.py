import pyblish.api


class ExtractReview(pyblish.api.InstancePlugin):
    """Extracts movie for review"""

    order = pyblish.api.ExtractorOrder
    label = "Review"
    optional = True
    hosts = ["nukestudio"]
    families = ["trackItem.ftrackEntity.shot"]

    def process(self, instance):
        import os
        import time
        import hiero.core

        nukeWriter = hiero.core.nuke.ScriptWriter()

        item = instance.data["item"]

        handles = instance.data["handles"]

        seq = item.parent().parent()
        root_node = hiero.core.nuke.RootNode(
            item.timelineIn() - handles,
            item.timelineOut() + handles,
            fps=seq.framerate()
        )
        nukeWriter.addNode(root_node)

        item.addToNukeScript(
            script=nukeWriter,
            includeRetimes=True,
            retimeMethod="Frame",
            startHandle=handles,
            endHandle=handles
        )

        output_path = os.path.abspath(
            os.path.join(
                instance.context.data["currentFile"], "..", "workspace"
            )
        )
        movie_path = os.path.join(
            output_path, "{0}_review.mov".format(instance.data["name"])
        )
        write_node = hiero.core.nuke.WriteNode(movie_path.replace("\\", "/"))
        write_node.setKnob("file_type", "mov")
        write_node.setKnob("mov32_fps", seq.framerate())
        nukeWriter.addNode(write_node)

        nukescript_path = movie_path.replace(".mov", ".nk")
        nukeWriter.writeToDisk(nukescript_path)

        process = hiero.core.nuke.executeNukeScript(
            nukescript_path,
            open(movie_path.replace(".mov", ".log"), "w")
        )

        while process.poll() is None:
            time.sleep(0.5)

        assert os.path.exists(movie_path), "Creating review failed."

        instance.data["output_path"] = movie_path