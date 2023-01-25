from deta import Deta
import glob

deta = Deta("d0dok662_MZpN39BWREbccKTe38ZbvRdsxrRFd5YR")
samvidhan_bot = deta.Drive("samvidhan_bot")

#for file in glob.glob('*'):
 #   samvidhan_bot.put(file, path=file)

l = samvidhan_bot.get('Article 14.jpeg')
l