# The MIT License
#
# Copyright (c) 2007 Damon Kohler
# Copyright (c) 2015 Jonathan Le Roux (Modifications for Create 2)
# Copyright (c) 2015 Brandon Pomeroy
# Copyright (c) 2017 Kevin Walchko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from openInterface import midi_table


class Song(object):
	"""
	NOTE ABOUT SONGS: For some reason you cannot play a new song immediately after
	playing a different one, only the first song will play. You have to time.sleep()
	at least a fraction of a second for the speaker to process
	"""
	"""
	Not implementing this for now.
	"""
	# test sequence
	# self.SCI.send(self.config.data['opcodes']['start'],0)
	# raise NotImplementedError()

	def __init__(self, sci):
		self.SCI = sci

	def play_test_sound(self):
		"""
		written to figure out how to play sounds. creates a song with a playlist
		of notes and durations and then plays it through the speaker using a
		hilariously messy spread of concatenated lists
		"""
		noError = True
		# sets lengths of notes
		short_note = 8
		medium_note = 16
		long_note = 20

		# stores a 4 note song in song 3
		current_song = 3
		song_length = 4
		song_setup = [current_song, song_length]
		play_list = []

		# writes the song note commands to play_list
		# change these to change notes
		play_list.extend([midi_table['C#4'], medium_note])
		play_list.extend([midi_table['G4'], long_note])
		play_list.extend([midi_table['A#3'], short_note])
		play_list.extend([midi_table['A3'], short_note])

		# adds up the various commands and arrays
		song_play = [self.config.data['opcodes']['play'], current_song]
		play_sequence = [song_setup + play_list + song_play]

		# flattens array
		play_sequence = [val for sublist in play_sequence for val in sublist]

		if noError:
			self.SCI.send(self.config.data['opcodes']['song'], tuple(play_sequence))
		else:
			raise Exception("Invalid data, failed to send")

	def create_song(self, song_number, play_list):
		"""
		create a new song from a playlist of notes and durations and tells the robot about it. Note: no error checking for playlist accuracy (must be a series of note opcodes and durations)
		"""
		noError = True

		# the length of the song is the length of the array divided by 2
		song_setup = [song_number, len(play_list)/2]
		play_list = [song_setup + play_list]
		play_list = [val for sublist in play_list for val in sublist]

		if noError:
			self.SCI.send(self.config.data['opcodes']['song'], tuple(play_list))
		else:
			raise Exception("Invalid data, failed to send")

	def play(self, song_number):
		"""
		Plays a stored song
		"""
		noError = True

		if noError:
			self.SCI.send(self.config.data['opcodes']['play'], tuple([song_number]))
		else:
			raise Exception("Invalid data, failed to send")

	def play_note(self, note_name, note_duration):
		"""Plays a single note by creating a 1 note song in song 0
		"""
		current_song = 0
		play_list = []
		noError = True
		if noError:
			# Need to map ascii to numbers from the dict.

			if note_name in midi_table:
				play_list.append(midi_table[note_name])
				play_list.append(note_duration)
			else:
				# That note doesn't exist. Plays nothing
				# Raise an error so the software knows that the input was bad
				play_list.append(midi_table[0])
				# warnings.formatwarning = custom_format_warning
				# warnings.warn("Warning: Note '" + note_name + "' was not found in midi table")
				raise Exception("Warning: Note '" + note_name + "' was not found in midi table")
			# create a song from play_list and play it
			self.create_song(current_song, play_list)
			self.play(current_song)

	def play_song(self, song_number, note_string):
		"""
		Creates and plays a new song based off a string of notes and durations.
		note_string - a string of notes,durations
		for example: 'G5,16,G3,16,A#4,30'
		"""
		# splits the string of notes and durations into two lists
		split_list = note_string.split(',')
		note_list = split_list[0::2]
		duration_list = split_list[1::2]
		# creates a list for serial codes
		play_list = []
		# convert the durations to integers
		duration_list = map(int, duration_list)
		noError = True

		# display_string = []

		if noError:
			# Need to map midi to numbers from the dict.
			# for note in note_list:  FIXME
			for i in range(0, len(note_list)):
				# Check that the note is in the list, if it is, add it.
				if note_list[i] in midi_table:
					play_list.append(midi_table[note_list[i]])
					play_list.append(duration_list[i])
				else:
					# Note was not available. Play a rest
					# Raise an error so the software knows that the input was bad
					play_list.append(midi_table['rest'])
					play_list.append(duration_list[i])
					# warnings.formatwarning = custom_format_warning
					# warnings.warn("Warning: Note '" + display_string[i] + "' was not found in midi table")
					raise Exception("Warning: Note '" + note_list[i] + "' was not found in midi table")

			# play the song
			self.create_song(song_number, play_list)
			self.play(song_number)
		else:
			raise Exception("Invalid data, failed to send")
