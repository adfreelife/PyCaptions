import re


metric = {
    "h" : 3_600_000_000,
    "m" : 60_000_000,
    "s" : 1_000_000,
    "ms" : 1_000
}


class MicroTime:
    def __init__(self, microseconds: int = 0, milliseconds: int = 0, seconds: int = 0,
                 minutes: int = 0, hours: int = 0):
        self.microseconds = microseconds
        self.milliseconds = milliseconds
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours

    @property
    def milli(self):
        return self.milliseconds

    @milli.setter
    def milli(self, value):
        self.milliseconds = value

    @property
    def micro(self):
        return self.microseconds

    @micro.setter
    def micro(self, value):
        self.microseconds = value

    def __str__(self) -> str:
        return f"{self.hours}h {self.minutes}m {self.seconds}s {self.milli}ms {self.micro}us"
    
    def __eq__(self, other):
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        return (
            self.microseconds == other.microseconds and
            self.milliseconds == other.milliseconds and
            self.seconds == other.seconds and
            self.minutes == other.minutes and
            self.hours == other.hours
        )

    def __ne__(self, other):
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        return (
            (self.hours, self.minutes, self.seconds, self.milliseconds, self.microseconds) <
            (other.hours, other.minutes, other.seconds, other.milliseconds, other.microseconds)
        )

    def __le__(self, other):
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        return (
            (self.hours, self.minutes, self.seconds, self.milliseconds, self.microseconds) <=
            (other.hours, other.minutes, other.seconds, other.milliseconds, other.microseconds)
        )

    def __gt__(self, other):
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        return (
            (self.hours, self.minutes, self.seconds, self.milliseconds, self.microseconds) >
            (other.hours, other.minutes, other.seconds, other.milliseconds, other.microseconds)
        )

    def __ge__(self, other):
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        return (
            (self.hours, self.minutes, self.seconds, self.milliseconds, self.microseconds) >=
            (other.hours, other.minutes, other.seconds, other.milliseconds, other.microseconds)
        )

    def __add__(self, other):
        if isinstance(other, int):
            result = MicroTime()
            result.milli, result.micro = divmod(self.micro+other, 1_000)
            result.seconds, result.milli = divmod(self.milli+result.milli, 1_000)
            result.minutes, result.seconds = divmod(self.seconds+result.seconds, 60)
            result.hours, result.minutes = divmod(self.minutes+result.minutes, 60)
            result.hours+=self.hours
            return result
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        result = MicroTime()
        result.milli, result.micro = divmod(self.micro+other.micro, 1_000)
        result.seconds, result.milli = divmod(self.milli+other.milli+result.milli, 1_000)
        result.minutes, result.seconds = divmod(self.seconds+other.seconds+result.seconds, 60)
        result.hours, result.minutes = divmod(self.minutes+other.minutes+result.minutes, 60)
        result.hours+=self.hours+other.hours
        return result
    
    def __iadd__(self, other):
        if isinstance(other, int):
            milli, self.micro = divmod(self.micro+other, 1_000)
            seconds, self.milli = divmod(self.milli+milli, 1_000)
            minutes, self.seconds = divmod(self.seconds+seconds, 60)
            hours, self.minutes = divmod(self.minutes+minutes, 60)
            self.hours+=hours
            return self
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        milli, self.micro = divmod(self.micro+other.micro, 1_000)
        seconds, self.milli = divmod(self.milli+other.milli+milli, 1_000)
        minutes, self.seconds = divmod(self.seconds+other.seconds+seconds, 60)
        hours, self.minutes = divmod(self.minutes+other.minutes+minutes, 60)
        self.hours+=hours+other.hours
        return self
    
    def __sub__(self, other):
        if isinstance(other, int):
            time = self.toTime()-other
            if time < 0:
                print("Time cannot be negative")
                return MicroTime()
            return MicroTime.fromTime(time)
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        time = self.toTime()-other.toTime()
        if time < 0:
            print("Time cannot be negative")
            return MicroTime()
        return MicroTime.fromTime(time)
    
    def __isub__(self, other):
        if isinstance(other, int):
            time = self.toTime()-other
            if time < 0:
                self._zero()
                print("Time cannot be negative")
            else:
                self._fromTime(time)    
            return self
        if not isinstance(other, MicroTime):
            raise TypeError(f"Unsupported operand type for +: {type(other)}")
        time = self.toTime()-other.toTime()
        if time < 0:
            self._zero()
            print("Time cannot be negative")
        else:
            self._fromTime(time)    
        return self
    
    def _zero(self):
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.milli = 0
        self.micro = 0

    def toTime(self) -> int:
        return (self.micro + self.milli*1_000 + self.seconds*1_000_000 
                + self.minutes*60_000_000 + self.hours*3_600_000_000)
    
    def _fromTime(self, time: int):
        self.hours, reminder = divmod(time, 3_600_000_000)
        self.minutes, reminder = divmod(reminder, 60_000_000)
        self.seconds, reminder = divmod(reminder, 1_000_000)
        self.milliseconds, self.microseconds = divmod(reminder, 1_000)
        
    
    @staticmethod 
    def fromTime(time: int):
        hours, reminder = divmod(time, 3_600_000_000)
        minutes, reminder = divmod(reminder, 60_000_000)
        seconds, reminder = divmod(reminder, 1_000_000)
        milliseconds, microseconds = divmod(reminder, 1_000)
        return MicroTime(microseconds=microseconds,milliseconds=milliseconds,
                         seconds=seconds,minutes=minutes,hours=hours)

    @staticmethod
    def fromSRTTime(time: str):
        return MicroTime(hours=int(time[0:2]), minutes=int(time[3:5]), 
                         seconds=int(time[6:8]), milliseconds=int(time[9:]))

    def toSRTTime(self) -> str:
        return f"{int(self.hours):02}:{int(self.minutes):02}:{int(self.seconds):02},{int(self.milli):03}"

    @staticmethod
    def fromVTTTime(time: str):
        seconds = 0
        minutes = 0
        hours = 0
        t = time[:-4].split(":")
        if len(t) == 3:
            hours = t[0]
            minutes = t[1]
            seconds = t[2]
        else:
            minutes = t[0]
            seconds = t[1]
        return MicroTime(milliseconds=int(time[-3:]), seconds=seconds, minutes=minutes, hours=hours)

    def toVTTTime(self) -> str:
        return f"{int(self.hours):02}:{int(self.minutes):02}:{int(self.seconds):02}.{int(self.milli):03}"

    @staticmethod
    def fromSUBTime(time: str, frame_rate: int):
        return MicroTime.fromTime(int(time) * 1_000_000 / frame_rate)

    def toSUBTime(self, frame_rate: int):
        return int(self.toTime() * frame_rate / 1_000_000)

    @staticmethod
    def parseTTMLTime(time: str, **kwargs):
        multiplier = metric.get(time[-1]) or kwargs.get(time[-1])
        if multiplier:
            return MicroTime.fromTime(float(time[:-1])*multiplier)
        else:
            time = time.split(":")
            hours = int(time[0])
            minutes = int(time[1])
            if len(time) == 3:
                seconds, milli = time[2].split(".")
                return MicroTime(hours=hours, minutes=minutes, 
                                 seconds=int(seconds), milliseconds=int(milli))
            else:
                seconds = int(time[2])
                if kwargs.get("subFrameRate"):
                    frames = time[3].split(".")
                    milli = frames[0] * 1_000_000 / kwargs.get("frameRate") 
                    milli += frames[1] * 1_000 / kwargs.get("subFrameRate")
                else:
                    milli = float(time[3]) * 1_000_000 / kwargs.get("frameRate")
                return MicroTime(hours=hours, minutes=minutes, seconds=seconds,
                                 milliseconds=int(milli), microseconds=(milli%1)*1_000)

  
    @staticmethod
    def fromTTMLTime(begin: str, dur: str, end: str, **kwargs):
        if begin:
            begin = MicroTime.parseTTMLTime(begin)
        else:
            begin = MicroTime()
        if dur:
            end = begin + MicroTime.parseTTMLTime(dur)
        else:
            if end:
                end = MicroTime.parseTTMLTime(end)
            else:
                end = MicroTime()
        return begin, end
    
    def toTTMLTime(self):
        return self.toVTTTime()
