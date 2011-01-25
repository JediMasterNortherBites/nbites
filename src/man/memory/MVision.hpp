/**
 * MVision.hpp
 *
 * @class MVision : this is the memory object representation of vision
 *
 */

#pragma once

#include <boost/shared_ptr.hpp>

#include "gen/Vision.pb.h"
#include "MObject.hpp"
#include "Vision.h"
#include "log/FileLogger.hpp"

//class MVision;

namespace memory {
class MVision: public proto::PVision, public MObject {

public:
    /**
     * @param v : the shared pointer to the instance of vision this MVision
     * links to
     * @return
     */
    MVision(boost::shared_ptr<Vision> v);
    ~MVision();
    /**
     * Updates all the fields of the underlying proto::PVision with values
     * from the Vision object
     */
    void update();
    void log() const;

private:
    boost::shared_ptr<Vision> vision;
    log::FileLogger* fileLogger;

};
}
