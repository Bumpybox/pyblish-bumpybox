import os
import re

import pyblish.api
import hiero


class ExtractPRORES(pyblish.api.Extractor):

    families = ['transcode_prores.trackItem']
    label = 'Transcode to PRORES'

    def get_path(self, shot, track_name, context):

        ftrack_data = context.data('ftrackData')

        path = [ftrack_data['Project']['root']]
        path.append('renders')
        path.append('movies')
        for p in reversed(shot.getParents()[:-1]):
            path.append(p.getName())

        path.append(shot.getName())
        path.append('transcode')

        # get version data
        version = 1
        if context.has_data('version'):
            version = context.data('version')
        version_string = 'v%s' % str(version).zfill(3)
        path.append(version_string)

        path.append('prores_%s' % track_name)

        filename = [shot.getName(), version_string, 'png']
        path.append('.'.join(filename))

        return os.path.join(*path).replace('\\', '/')

    def frames_to_timecode(self, frames, framerate):

        h = str(int(frames / (3600 * framerate))).zfill(2)
        m = str(int(frames / (60 * framerate) % 60)).zfill(2)
        s = int(float(frames) / framerate % 60)
        f = float('0.' + str((float(frames) / framerate) - s).split('.')[1])
        f = int(f / (1.0 / framerate))

        return '%s:%s:%s:%s' % (h, m, str(s).zfill(2), str(f).zfill(2))

    def process(self, instance, context):

        item = instance[0]

        # skipping if not launched from ftrack
        if context.has_data('ftrackData'):
            import ftrack

            ftrack_data = context.data('ftrackData')
            parent = ftrack.Project(ftrack_data['Project']['id'])
            parent_path = [parent.getName()]

            if 'Episode' in ftrack_data:
                parent = ftrack.Sequence(ftrack_data['Episode']['id'])
                parent_path.append(parent.getName())

            naming = '([a-z]+[0-9]{3})'
            names = re.findall(naming, item.name())
            if len(names) > 1:
                [sequence_name, shot_name] = names
            else:
                shot_name = names[0]
                if 'Sequence' in ftrack_data:
                    sequence_name = ftrack_data['Sequence']['name']
                else:
                    sequence_name = item.sequence().name()

            parent_path.append(sequence_name)
            parent_path.append(item.name())

            shot = ftrack.getShot(parent_path)

            output_path = self.get_path(shot,
                                    instance.data('videoTrack').name(), context)

            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))

        # collecting output data
        basename = os.path.splitext(os.path.basename(output_path))[0]
        filename = '.'.join([basename, 'mov'])
        output_path = os.path.join(os.path.dirname(output_path), filename)

        if context.has_data('ftrackData'):
            asset = shot.createAsset('transcode', 'mov')
            version = None
            for v in asset.getVersions():
                if v.getVersion() == context.data('version'):
                    version = v

            if not version:
                version = asset.createVersion()
                version.set('version', value=context.data('version'))

            version.publish()

            try:
                name = 'prores_%s' % instance.data('videoTrack').name()
                version.createComponent(name=name, path=output_path)
            except:
                msg = 'Component "%s" already exists. ' % name
                msg += 'Please delete it manually first.'
                self.log.warning(msg)

        # adding deadline data
        job_data = {'Group': 'ffmpeg','Pool': 'medium',
                    'Plugin': 'FFmpeg', 'OutputFilename0': output_path,
                    'Frames': 0}

        plugin_data = {'InputArgs0': '', 'OutputFile': output_path,
                            'ReplacePadding': False, 'UseSameInputArgs': False}

        args = '-codec prores -vf lutrgb=r=gammaval(0.45454545)'
        args += ':g=gammaval(0.45454545):b=gammaval(0.45454545)'
        start_frame = item.source().sourceIn()
        fps = item.sequence().framerate().toFloat()
        args += ' -timecode %s' % self.frames_to_timecode(start_frame, fps)
        plugin_data['OutputArgs'] = args

        input_path = item.source().mediaSource().fileinfos()[0].filename()
        plugin_data['InputFile0'] = input_path

        data = {'job': job_data, 'plugin': plugin_data}
        instance.set_data('deadlineData', value=data)